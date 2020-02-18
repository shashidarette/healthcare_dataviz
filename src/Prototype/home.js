var ccgData = [];
var focusedItems = [];

// load CCG details for mapping with CCG id
function loadCCGDetails() {
    $.getJSON('./ccg.json', function (ccgDetails) {
        if (ccgDetails != null) {
            for (var index = 0; index < ccgDetails.length; index++) {
                var code = ccgDetails[index].code;
                ccgData[code] = ccgDetails[index].name;
            }
        }
    })
}

// reset search status
function resetSearchStatus() {
    $('#welcome_msg').hide();
    $('#focus_group_div').show();
    $('#search_list').empty();
}

// add the search elements
function addSearchElement(searchEntry) {
    if (searchEntry.type === 'Practice') {
        var name = searchEntry.name;
        var code = searchEntry.code;
        var postcode = searchEntry.postcode;
        var ccg = ccgData[searchEntry.ccg];
        var searchList = $('#search_list');

        var item = $('<a href="#" class="list-group-item list-group-item-action flex-column align-items-start">').text(name);
        item.append('   ');
        item.append(getButtonGroup())
        item.append(getPracticeInfo(code, postcode, ccg))
        item.attr('id', code);
        searchList.append(item);
    }
}

// create teh practice info element
function getPracticeInfo(code, postcode, ccg) {
    var p = $('<p>');
    p.append($('<b>').text('PracticeCode: '));
    p.append(code); p.append($('<br/>'));
    p.append($('<b>').text('CCG: '));
    p.append(ccg); p.append($('<br/>'));
    p.append($('<b>').text('Postcode: '))
    p.append(postcode); p.append($('<br/>'));
    return p;
}

// add the button group for additional funcitonalities for each entry
function getButtonGroup() {
    var buttonGroup = $('<div class="btn-group btn-group-sm">' +
                                        '<button type="button" class="btn btn-primary" onclick="onAddFocus(this)">Add to focus</button>' +
                                        '<button type="button" class="btn btn-primary" onclick="onRemoveFocus(this)">Remove focus</button>' +
                                        '<button type="button" class="btn btn-primary" onclick="onViewTrends(this)">View trends</button>' +
                                    '</div>');
    return buttonGroup;
}


function getParentId(object) {
    var parent = object.closest("a");
    return parent.id;
}

// Array Remove - By John Resig (MIT Licensed)
Array.prototype.remove = function(from, to) {
    var rest = this.slice((to || from) + 1 || this.length);
    this.length = from < 0 ? this.length + from : from;
    return this.push.apply(this, rest);
};

// add focus
function onAddFocus(object) {
    var id = getParentId(object);
    var item = $('<li class="list-group-item">').text(id);
    item.attr('id', id);
    $('#focus_group').append(item);
    focusedItems.push(id);
}

// remove focus
function onRemoveFocus(object) {
    var id = getParentId(object);
    var item = $('#focus_group li#' + id);
    if (item != undefined) {
        item.remove();
        var index = focusedItems.findIndex(fid => fid === id);
        if (index != undefined && index > -1) {
            focusedItems.remove(index);
        }
    }
}

// open view trends page in a new window
function onViewTrends(object) {
    var id = getParentId(object);
    var query = '?org=' + id;
    window.open('ViewTrends.html' + query);
}

// open view focus page in a new window
function onViewFocusGroup(object) {
    if (focusedItems != undefined) {
        var count = focusedItems.length;
        if (count > 0) {
            if (count > 4) {
                alert('Only top 4 items will be considered for focus group.');
            }
            var query = '?org=' + focusedItems.join();
            window.open('ViewFocusGroup.html' + query);
        } else {
            alert('Please add items of interest to focus group.');
        }
    }
}

// intialize on document ready
$(document).ready(function () {
    $("#focus_group_div").hide();
    addEnterKeyHandlerForSearch();
    loadGPProfiles();
    loadCCGDetails();
})