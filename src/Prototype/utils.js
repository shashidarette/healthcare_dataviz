// This script is for utility functions
function getQueryParams(queryString) {
    var params = {};
    var queryParams = queryString.split("&");
    var count = queryParams.length;

    for (var index = 0; index < count; index++) {
        var p = queryParams[index].split('=');
        // param and value
        params[p[0]] = p[1];
    }
    return params;
};

function getQueryOrgs() {
    // get the url parameters passed
    var queryString = window.location.search;
    queryString = queryString.substring(1);

    var params = getQueryParams(queryString);
    return params['org'].split(',');
}