require([
    'underscore',
    'jquery',
    'splunkjs/mvc',
    'splunkjs/mvc/tableview',
    'splunkjs/mvc/simplexml/ready!'
], function(_, $, mvc, TableView) {
    var ICONS = {
        0: 'plus-circle',
        1: 'minus-circle'
    };
    var RANGE = {
        0: 'green',
        1: 'red'
    };
    var invICONS = {
        'plus-circle': 0,
        'minus-circle': 1
    };
    var RangeMapIconRenderer = TableView.BaseCellRenderer.extend({
        canRender: function(cell) {
            // Only use the cell renderer for the range field
            return cell.field === 'status';
        },
        render: function($td, cell) {
            var icon = "plus-circle";
            var range = "green";

            // Fetch the icon for the value
            if (ICONS.hasOwnProperty(cell.value)) {
                icon = ICONS[cell.value];
                range = RANGE[cell.value];
            }
            // Create the icon element and add it to the table cell
            $td.addClass('icon').html(_.template('<i class="icon-<%-icon%> <%- range %> click"></i>', {
                icon: icon,
                range: range
            }));
            $td.on("click", function(e){
                var i = $(this.firstChild);
                i.removeClass("icon-" + icon);
                i.removeClass(range);
                i.addClass('icon-rotate');
                i.addClass('blue');
                i.addClass('spin');
                // ajax call to kick off createdist or pydelete, include callback to reload page
                // determine create or delete
                var search;
                if (range === "green") {
                    search = "| createdist version=" + i.parent().parent().children()[1].innerHTML;
                } else if (range === "red") {
                    search = "| pydelete " + i.parent().parent().children()[1].innerHTML;
                }
                $.post(location.origin + "/en-US/splunkd/__raw/servicesNS/nobody/pyden-manager/search/jobs", {'exec_mode': 'oneshot', 'search': search}, function (data) {
                    var serializer = new XMLSerializer()
                    var dataString = serializer.serializeToString(data)
                    i.removeClass('icon-rotate');
                    i.removeClass('blue');
                    i.removeClass('spin');
                    var oldValue = invICONS[icon];
                    var newValue = (dataString.includes("Successfully compiled Python") || dataString.includes("Successfully deleted")) ? (oldValue + 1) % 2 : oldValue;
                    icon = ICONS[newValue];
                    range = RANGE[newValue];
                    i.addClass('icon-' + icon);
                    i.addClass(range);
                    i.addClass('click');
                    if (oldValue === newValue) {
                        alert("Python failed to compile. Review pyden.log for errors.")
                    }
                })
            });
        }
    });
    mvc.Components.get('version_table').getVisualization(function(tableView){
        // Register custom cell renderer, the table will re-render automatically
        tableView.addCellRenderer(new RangeMapIconRenderer());
    });
    $('#submit > button').on("click", function (e) {
        // run search to set default to input token value and reload on succesfull callback
        var tokens = mvc.Components.get("default");
        var version_default = tokens.get("version_default");
        var job_url = location.origin + "/" + location.href.split("/")[3] + "/splunkd/__raw/servicesNS/nobody/pyden-manager/search/jobs";
        var params = {
            "exec_mode": "blocking",
            "search": "| changedefaultpys distribution=" + version_default
        };
        $.post(job_url, params, function() {window.location = window.location.href.split("?")[0];})
    });
});