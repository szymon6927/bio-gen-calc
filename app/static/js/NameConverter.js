function converterName(name) {
  if (name === "chi2_standard") {
    return "Chi square";
  }
  else if (name === "chi_square") {
    return "Chi square";
  }
  else if (name === "chi2_yats") {
    return "Yate`s Chi square";
  }
  else if (name === "dof") {
    return "dof";
  }
  else if (name === "p_standard") {
    return "Chi square p-value";
  }
  else if (name === "p_yats") {
    return "Yate`s Chi square p-value";
  }
  else if (name === "corelation_yats") {
    return "Yate`s chi-square correlation";
  }
  else if (name === "corelation_standard") {
    return "Chi-square correlation";
  }
  else {
    return name;
  }
}