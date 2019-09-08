import base64
import itertools
import json
from io import BytesIO

import graphviz
import joblib
import pandas as pd
import scipy.stats as stats
import seaborn as sns
from flask import render_template
from sklearn import tree

from app.apmc.ds.common.enums import ModelTypeChoices
from app.apmc.ds.processing.data_processing import prepare_data_for_report
from app.apmc.models import APMCData


class ReportGenerator:
    RANDOM_FOREST_NAMES = ["Random forest classification", "Random forest regression"]

    def __init__(self, apmc_data: APMCData):
        self.apmc_data = apmc_data
        self.prepared_data = prepare_data_for_report(self.apmc_data.dataset_path())

    def _get_model_name(self):
        model_metrics = json.loads(self.apmc_data.model_metrics)

        return model_metrics.get('model_name')

    def _get_model(self):
        return joblib.load(self.apmc_data.model_path())

    def _convert_to_base64(self, figure):
        """ Convert seaborn, matplotlib figure to base64

        :param figure: Seaborn or Matplotlib figure like object
        :return: base64 encoded data
        """
        figfile = BytesIO()

        figure.savefig(figfile)

        figfile.seek(0)

        figdata_png = base64.b64encode(figfile.getvalue())
        decoded_figdata_png = figdata_png.decode('utf-8')

        return decoded_figdata_png

    def get_basic_statistic(self):
        """Method to get basic statistic"""
        desc_data = self.prepared_data.get('data').describe()

        return desc_data.to_html()

    def get_coefficients_table(self):
        """method to get coefficients table based on model"""
        if self.apmc_data.model_type == ModelTypeChoices.regression:
            model = self._get_model()
            predictors_names = self.prepared_data.get('predictors_names')

            if self._get_model_name() in self.RANDOM_FOREST_NAMES:
                coef = model.feature_importances_
            else:
                coef = model.coef_

            frame_coef = pd.DataFrame(coef, columns=["Coefficients"], index=predictors_names)

            return frame_coef.to_html()

        return None

    def get_tree_graph(self):
        if self._get_model_name() in self.RANDOM_FOREST_NAMES:
            model = self._get_model()
            predictors_names = self.prepared_data.get('predictors_names')
            classes = self.prepared_data.get('classes')

            # get best tree from forest
            one_tree = model.estimators_[5]  # temporary solution

            dot_data = tree.export_graphviz(
                one_tree,
                out_file=None,
                feature_names=predictors_names,
                class_names=classes,
                filled=True,
                rounded=True,
                special_characters=True,
            )

            graph = graphviz.Source(dot_data, format='svg')
            graph_svg = graph.pipe().decode('utf-8')

            return graph_svg

        return None

    def _generate_relation_plot_classification(self):
        # Generate violin-plot y_var vs all
        col_names = self.prepared_data.get('col_names')
        data = self.prepared_data.get('data')

        quantitive_loc = col_names[-1]  # y_var
        col_names.remove(quantitive_loc)

        value_vs_predictors_plots = []
        predictors_vs_predictors_plots = []

        for predictor in col_names:
            plot = sns.violinplot(data=data, x=quantitive_loc, y=predictor)
            fig = plot.get_figure()

            value_vs_predictors_plots.append(self._convert_to_base64(fig))

            fig.clear()

        # Generate plot all predictors vs all predictores

        data_combinations = list(itertools.combinations(col_names, 2))

        for var_x, var_y in data_combinations:
            x_ax = data[var_x]
            y_ax = data[var_y]

            sns.set(style="darkgrid")
            plot = sns.jointplot(x=x_ax, y=y_ax, kind='reg').annotate(stats.pearsonr)

            predictors_vs_predictors_plots.append(self._convert_to_base64(plot))

        return value_vs_predictors_plots, predictors_vs_predictors_plots

    def _generate_relation_plot_regression(self):
        col_names = self.prepared_data.get('col_names')
        data = self.prepared_data.get('data')

        data_combinations = list(itertools.combinations(col_names, 2))

        plots = []

        for var_x, var_y in data_combinations:
            x_ax = data[var_x]
            y_ax = data[var_y]

            plot = sns.jointplot(x=x_ax, y=y_ax, kind='reg').annotate(stats.pearsonr)

            plots.append(self._convert_to_base64(plot))

        return plots

    def generate_relation_plot(self):
        """Method to generate relation-plot between all vs all in data"""

        sns.set(style="darkgrid")

        if self.apmc_data.model_type == ModelTypeChoices.regression:
            return self._generate_relation_plot_regression()

        if self.apmc_data.model_type == ModelTypeChoices.classification:
            return self._generate_relation_plot_classification()

        return None

    def generate_report(self):
        data = {
            'apmc_data': self.apmc_data,
            'model_name': self._get_model_name(),
            'basic_statistic': self.get_basic_statistic(),
            'relation_plots': self.generate_relation_plot(),
            'coefficients_table': self.get_coefficients_table(),
            'tree_graph': self.get_tree_graph(),
        }

        template = render_template('userpanel/apmc/statistical_report.html', context=data)

        return template