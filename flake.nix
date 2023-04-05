# THis is my current flake.nix but I am getting the following error
{
  inputs = {
    nixpkgs = {
      url = "github:nixos/nixpkgs/nixos-unstable";
    };
    flake-utils = {
      url = "github:numtide/flake-utils";
    };
    cmaps-src = {
      url = "github:hhuangwx/cmaps";
    };
  };
  outputs = {
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {
          inherit system;
        };
        inherit (pkgs) stdenv lib;

        pythonPackages = lib.fix' (self:
          with self;
            pkgs.python3Packages
            // {
              cartopy = buildPythonPackage rec {
                pname = "cartopy";
                version = "0.21.0";

                src = fetchPypi {
                  inherit pname version;
                  sha256 = "sha256-zh06KKEy6UyJrDN2mlD4H2VjSrK9QFVjF+Fb1srRzkI=";
                };

                postPatch = ''
                  # https://github.com/SciTools/cartopy/issues/1880
                  substituteInPlace lib/cartopy/tests/test_crs.py \
                    --replace "test_osgb(" "dont_test_osgb(" \
                    --replace "test_epsg(" "dont_test_epsg("
                '';

                nativeBuildInputs = [
                  cython
                  geos # for geos-config
                  proj
                  setuptools-scm
                ];

                buildInputs = [
                  geos
                  proj
                ];

                propagatedBuildInputs = [
                  # required
                  six
                  pyshp
                  shapely
                  numpy

                  # optional
                  gdal
                  pillow
                  matplotlib
                  pyepsg
                  pykdtree
                  scipy
                  fiona
                  owslib
                ];

                checkInputs = [pytestCheckHook filelock mock pep8 flufl_lock];
                pytestFlagsArray = [
                  "--pyargs"
                  "cartopy"
                  "-m"
                  "'not network and not natural_earth'"
                ];

                disabledTests = [
                  "test_nightshade_image"
                  "background_img"
                  "test_gridliner_labels_bbox_style"
                ];
              };

              cmaps = buildPythonPackage rec {
                pname = "cmaps";
                version = "0.1.0";
                src = cmaps-src;
                meta = with pkgs.stdenv.lib; {
                  description = "Colormaps for scientific visualization.";
                  homepage = "https://github.com/hhuangwx/cmaps";
                  license = licenses.mit;
                  maintainers = [maintainers.yourname];
                };
              };
              # geocat.viz =  buildPythonPackage rec {
              # metpy =  buildPythonPackage rec {
            });
      in rec {
        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            (python3.withPackages (ps:
              with ps; [
                certifi
                charset-normalizer
                click
                wheel
                # cartopy
                # cmaps
                # geocat.viz
                # metpy
                contourpy
                cycler
                flask
                fonttools
                geos
                idna
                itsdangerous
                jinja2
                joblib
                kiwisolver
                lxml
                markupsafe
                matplotlib
                numpy
                packaging
                pandas
                pillow
                pint
                platformdirs
                pooch
                pyparsing
                pyproj
                pyshp
                python-dateutil
                pytz
                requests
                scikit-learn
                scipy
                shapely
                six
                threadpoolctl
                traitlets
                urllib3
                werkzeug
                xarray
              ]))
          ];
          shellHook = "python ./webapp.py";
        };
      }
    );
}
