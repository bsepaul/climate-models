{
  inputs = {
    nixpkgs = {
      url = "github:nixos/nixpkgs/nixos-unstable";
    };
    flake-utils = {
      url = "github:numtide/flake-utils";
    };
  };
  outputs = {
    nixpkgs,
    flake-utils,
    ...
  } @ inputs:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {
          inherit system;
        };

        lib = import flake-utils.lib {inherit pkgs;};
        # inherit (pkgs) stdenv lib;
        inherit (pkgs) stdenv ;

        metpy = inputs.nixpkgs.lib.overrideDerivation (oldDrv: {
          pname = "metpy";
          version = "1.0.1";
          src = inputs.nixpkgs.fetchFromGitHub {
            owner = "Unidata";
            repo = "MetPy";
            rev = "v1.0.1";
            sha256 = "sha256-FvqYBvrMJPMfRUuJh0HsVjmnK6nU/4oZrQ6UYp2Ty5U=";
          };
          buildInputs = with inputs.nixpkgs; [
            matplotlib
            numpy
            pandas
            pint
            pooch
            pyproj
            scipy
            traitlets
            xarray
            importlib-resources
            importlib-metadata
          ];
          doCheck = false;
        });

        cmaps = inputs.nixpkgs.lib.overrideDerivation (oldDrv: {
          pname = "cmaps";
          version = "1.0.5";
          src = inputs.nixpkgs.fetchFromGitHub {
            owner = "hhuangwx";
            repo = "cmaps";
            rev = "master";
            sha256 = "sha256-FvqYBvrMJPMfRUuJh0HsVjmnK6nU/4oZrQ6UYp2Ty5U=";
          };
          doCheck = false;
        });

        geocat = inputs.nixpkgs.lib.overrideDerivation (oldDrv: {
          pname = "geocat.viz";
          version = "0.9.1";
          src = inputs.nixpkgs.fetchFromGitHub {
            owner = "Unidata";
            repo = "MetPy";
            rev = "v1.0.1";
            sha256 = "sha256-FvqYBvrMJPMfRUuJh0HsVjmnK6nU/4oZrQ6UYp2Ty5U=";
          };
          buildInputs = with inputs.nixpkgs; [
            matplotlib
            numpy
            pandas
            pint
            pooch
            pyproj
            scipy
            traitlets
            xarray
            importlib-resources
            importlib-metadata
          ];
          doCheck = false;
        });

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
                cartopy
                # metpy
                # cmaps
                geocat
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
