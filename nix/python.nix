pkgs: self: super: rec {

  metpy = self.buildPythonPackage rec {
    pname = "MetPy";
    version = "1.0.1";
    src = self.fetchPypi {
      inherit pname version;
      sha256 = "sha256-FvqYBvrMJPMfRUuJh0HsVjmnK6nU/4oZrQ6UYp2Ty5U=";
    };
    propagatedBuildInputs = with self; [
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
    # The setuptools checks try to use the network which isn't allowed
    # during the Nix build. Disabling them for now.
    doCheck = false;
  };

}
