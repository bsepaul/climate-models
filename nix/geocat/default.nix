{}:
let
  nixpkgs = (fetchTarball "https://github.com/NixOS/nixpkgs/archive/0874168639713f547c05947c76124f78441ea46c.tar.gz");
  pkgs = import nixpkgs { };
  buildPythonPackage = pkgs.python3Packages.buildPythonPackage;
  fetchPypi = pkgs.python3Packages.fetchPypi;

  metpy = buildPythonPackage rec{
    pname = "MetPy";
    version = "1.4.1";
    src = fetchPypi {
      inherit pname version;
      hash = "sha256-oT3S2jYOv9hWJw5BdG5P1Uutyp3NvYASKegDgs4x27k=";
    };
    propagatedBuildInputs = with pkgs.python3Packages ;[ setuptools_scm pyproj numpy xarray pint scipy traitlets pooch matplotlib ];
  };
  cmaps = buildPythonPackage rec{
    pname = "cmaps";
    version = "1.0.5";
    src = fetchPypi {
      inherit pname version;
      hash = "sha256-jucIv2xAJNzQYNZYqgy7p0CsBHLlY4UStHZN6h6SjEY=";
    };
    propagatedBuildInputs = with pkgs.python3Packages ;[ numpy matplotlib ];
  };

  goecat-viz = pkgs.python3Packages.buildPythonPackage rec {
    pname = "geocat.viz";
    version = "2022.7.0";
    src = pkgs.python3Packages.fetchPypi {
      inherit pname version;
      sha256 = "sha256-7iBZitt+A/BJVsBahlVAtUfps1b0jKBBsqpPWBoqhPI=";
    };
    propagatedBuildInputs = with pkgs.python3Packages; [ cmaps metpy cartopy xarray scikit-learn pint traitlets pooch ];
  };
in
pkgs.mkShell {
  pname = "geocat-shell";
  buildInputs = [
    (pkgs.python3.withPackages (ps: [ goecat-viz ]))
  ];
}
