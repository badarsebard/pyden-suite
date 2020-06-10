"use strict";

var app_name = "pyden-manager";

require.config({
    paths: {
        PydenSetupView: "../app/" + app_name + "/pyden_setup_view",
    },
});

require([
    "backbone",
    "jquery",
    "PydenSetupView",
], function (Backbone, jquery, PydenSetupView) {
    var pyden_setup_view = new PydenSetupView({
        // Sets the element that will be used for rendering
        el: jquery("#main_container"),
    });
    var utils = require("splunkjs/mvc/utils");
    $(document).ready(function () {
        var l = document.getElementsByClassName("dashboard-title dashboard-header-title");
        l[0].innerHTML = "";
    });
    pyden_setup_view.render();
});