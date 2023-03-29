{
  inputs = {
    mach-nix.url = "mach-nix/3.5.0";
  };

  outputs = {
    self,
    nixpkgs,
    mach-nix,
  } @ inp: let
    l = nixpkgs.lib // builtins;
    supportedSystems = ["x86_64-linux" "aarch64-darwin"];
    forAllSystems = f:
      l.genAttrs supportedSystems
      (system: f system (import nixpkgs {inherit system;}));
  in {
    # enter this python environment by executing `nix shell .`
    defaultPackage = forAllSystems (system: pkgs:
      mach-nix.lib."${system}".mkPython {

        requirements = builtins.readFile ./requirements.txt;
        # requirements = ''
        #   pillow
        #   numpy
        #   requests
        # '';
      });
  };
}
# {
#   inputs = {
#     nixpkgs = {
#       url = "github:nixos/nixpkgs/nixos-unstable";
#     };
#     flake-utils = {
#       url = "github:numtide/flake-utils";
#     };
#   };
#   outputs = {
#     nixpkgs,
#     flake-utils,
#     ...
#   }:
#     flake-utils.lib.eachDefaultSystem (
#       system: let
#         pkgs = import nixpkgs {
#           inherit system;
#         };
#       in rec {
#         devShell = pkgs.mkShell {
#           buildInputs = with pkgs; [
#             (python3.withPackages (ps:
#               with ps; [
#                 Cartopy
#                 certifi
#                 charset-normalizer
#                 click
#                 cmaps
#                 contourpy
#                 cycler
#                 Flask
#                 fonttools
#                 geocat.viz
#                 geos
#                 idna
#                 itsdangerous
#                 Jinja2
#                 joblib
#                 kiwisolver
#                 lxml
#                 MarkupSafe
#                 matplotlib
#                 MetPy
#                 numpy
#                 packaging
#                 pandas
#                 Pillow
#                 Pint
#                 platformdirs
#                 pooch
#                 pyparsing
#                 pyproj
#                 pyshp
#                 python-dateutil
#                 pytz
#                 requests
#                 scikit-learn
#                 scipy
#                 shapely
#                 six
#                 threadpoolctl
#                 traitlets
#                 urllib3
#                 Werkzeug
#                 xarray
#               ]))
#           ];
#           shellHook = "flask run";
#         };
#       }
#     );
# }

