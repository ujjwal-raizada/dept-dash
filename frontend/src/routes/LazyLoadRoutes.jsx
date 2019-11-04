import React from "react";
import Loadable from "react-loadable";

const loading = <div>Loading...</div>;

export const Home = Loadable({
  "loader": () => import("../components/Home"),
  "loading": () => loading
});

export const ErrorPage404 = Loadable({
  "loader": () => import("../components/404"),
  "loading": () => loading
});
