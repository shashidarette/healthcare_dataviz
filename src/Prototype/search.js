// This is the java-script file with client logic specific for Search functionality
// used Organisation codes from "OpenPrescribing.net, EBM DataLab, University of Oxford, 2017"
// https://openprescribing.net/api/1.0/org_code/?format=json&q=victoria

var url = 'https://openprescribing.net/api/1.0/org_code/?format=json&';

// process the search results and add entries
function processResults(data, searchSting) {
    if (data != undefined) {
        resetSearchStatus();
        for (var index = 0; index < data.length; index++) {
            addSearchElement(data[index]);
        }
    }
}

// report failure message
function fail() {
    alert('Search operation failed! Please retry.')
}

// run the search for the given search string
function runSearch(searchString) {
    $.ajax({
        url: url,
        data: {
            q: searchString
        },
        success: function (data) {
            processResults(data, searchString);
        },
        fail: fail,
    });
}

// on search click
function onSearchClick(object) {
    var searchString = $('#search_string').val();
    runSearch(searchString);
}

// Handle enter event  : referred w3school tutorial
var ENTER_RETURN_KEY = 13;
function addEnterKeyHandlerForSearch() {
    var searchString = $('#search_string');

    searchString.on("keyup", function (event) {
        // supress default event
        event.preventDefault();
        if (event.keyCode === ENTER_RETURN_KEY) {
            onSearchClick(searchString)
        }
    });
}