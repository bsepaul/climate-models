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
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {
          inherit system;
        };
      in rec {
        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            (python3.withPackages (ps:
              with ps; [
                certifi
                charset-normalizer
                click
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

