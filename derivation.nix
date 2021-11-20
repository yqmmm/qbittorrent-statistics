{ lib, python3Packages }:
with python3Packages;
buildPythonApplication {
  pname = "qbittorrent-statistics";
  version = "0.1";
  propagatedBuildInputs = [
    requests
    python-pushover 
    matplotlib
  ];
  src = ./.;
}
