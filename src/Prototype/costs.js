// for prescription costs : uses spending api from "OpenPrescribing.net, EBM DataLab, University of Oxford, 2017"
// https://openprescribing.net/api/1.0/spending_by_practice/?code=0704050&org=G85034,M85063&date=2016-08-01
var url = 'https://openprescribing.net/api/1.0/spending_by_practice/?format=json&';
var drugGroupId = null;
var drugGroupSelected = [];
var drugGroupCosts = [];

// pre-defined trend dates for drug groups
var trend_dates =
    {
        'Jan 17': '2017-01-01',
        'Feb 17': '2017-02-01',
        'Mar 17': '2017-03-01',
        'Apr 17': '2017-04-01',
        'May 17': '2017-05-01',
        'Jun 17': '2017-06-01',
        'Jul 17': '2017-07-01',
        'Aug 17': '2017-08-01',
        'Sep 17': '2017-09-01',
        'Oct 17': '2017-10-01',
        'Nov 17': '2017-11-01',
        'Dec 17': '2017-12-01',
    }

var rev_trend_dates =
    {
        '2017-01-01': 'Jan 17',
        '2017-02-01': 'Feb 17',
        '2017-03-01': 'Mar 17',
        '2017-04-01': 'Apr 17',
        '2017-05-01': 'May 17',
        '2017-06-01': 'Jun 17',
        '2017-07-01': 'Jul 17',
        '2017-08-01': 'Aug 17',
        '2017-09-01': 'Sep 17',
        '2017-10-01': 'Oct 17',
        '2017-11-01': 'Nov 17',
        '2017-12-01': 'Dec 17',
    }

// pre-defined chapters
var chapters = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '19', '20', '21', '22', '23'];
// var chapters = ['Ch-01', 'Ch-02', 'Ch-03', 'Ch-04', 'Ch-05', 'Ch-06', 'Ch-07', 'Ch-08', 'Ch-09', 'Ch-10', 'Ch-11', 'Ch-12', 'Ch-13', 'Ch-14', 'Ch-15', 'Ch-19', 'Ch-20', 'Ch-21', 'Ch-22', 'Ch-23'];

//{
    //    '01': '01',
    //    '02': '02',
    //    '03': '03',
    //    '04': '04',
    //    '05': '05',
    //    '06': '06',
    //    '07': '07',
    //    '08': '08',
    //    '09': '09',
    //    '10': '10',
    //    '11': '11',
    //    '12': '12',
    //    '13': '13',
    //    '14': '14',
    //    '15': '15',
    //    //'16': '16',
    //    //'17': '17',
    //    //'18': '18',
    //    '19': '19',
    //    '20': '20',
    //    '21': '21',
    //    '22': '22',
    //    '23': '23',
    //}

var latest = {
     'Jan 18' : '2018-01-01',
    }

// used to defined end of ajax calls
var ajaxCostCalls = 0;

// process costs
function processCosts(data, code) {
    ajaxCostCalls--;
    for (index = 0; index < data.length; index++) {
        var practiceCode = data[index].row_id;
        var date = data[index].date;

        if (drugGroupCosts[practiceCode] == undefined) {
            drugGroupCosts[practiceCode] = [];
        }
        if (drugGroupCosts[practiceCode][code] == undefined) {
            drugGroupCosts[practiceCode][code] = [];
        }
        if (date != undefined) {
            if (drugGroupCosts[practiceCode][code][date] == undefined) {
                drugGroupCosts[practiceCode][code][date] = [];
            }
            drugGroupCosts[practiceCode][code][date] = data[index].actual_cost != undefined ? data[index].actual_cost : null;
        }
    }
    
    // update the cost plots
    if (ajaxCostCalls == 0) {
        // all calls complete : update the plots based on the data accumulated
        if (drugGroupId == null || drugGroupId == undefined) {
            // update chapters costs
            updateChapterpCostsPlot();
        } else {
            // update drug group costs plot
            updateGroupCostsPlot();
            drugGroupId = null;
        }
    }
};

var fail = function (data) {
    ajaxCostCalls--;
};

// get the costs from OpenPrescribing.net
var getCosts = function (org, code, month) {
    $.ajax({
        url: url,
        data: {
            org: org,
            code : code,
            date: month
        },
        success: function(data) {
            processCosts(data, code);
        },
        fail: fail,
    });
};

function getOrgs() {
    // hard-coded array as focus group items
    // return ['G85034', 'M85063'];
    return focusGroup;
}

// get costs
function getOrgCosts(orgs) {
    var org = orgs.join();
    // all chapters
    for (var index = 0; index < chapters.length; index++) {
        ajaxCostCalls++;
        getCosts(org, chapters[index], latest['Jan 18']);
    }
}

// update focus selection
function btnUpdateFocusSelection(object) {
    // get the practices added to focus group
    var orgs = getOrgs();
    if (orgs.length == 0) {
        alert('Please select practices as part of focus group.');
        return;
    }
    getOrgCosts(orgs);
}

// update drug group selection
function btnUpdateDrugGroupSelection(object) {
    // get the practices added to focus group
    var orgs = getOrgs();
    if (orgs.length == 0) {
        alert('Please select practices as part of focus group.');
        return;
    }
    var org = orgs.join();
    // check if a specific drug group is selected
    drugGroupSelected = $("#fg_drug_groups").val();
    drugGroupId = drugGroupSelected != null ? drugGroupSelected.join() : undefined; //;

    if (drugGroupId != undefined) {
        for (var dgIndex in drugGroupSelected) {
            var dg = getDrugGroupCode(drugGroupSelected[dgIndex]);
            for (var month in trend_dates) {
                ajaxCostCalls++;
                getCosts(org, dg, trend_dates[month]);
            }
        }
    }
}

// update chapters cost plot
function updateChapterpCostsPlot() {
    var traces = [];
    var chs = [];
    var month = latest['Jan 18'];
    var orgs = getOrgs();

    for (var index = 0; index < chapters.length; index++) {
        chs.push('ch' + chapters[index]);
    }

    for (var index = 0; index < orgs.length; index++) {
        var costs = [];
        for (var chIndex = 0; chIndex < chapters.length; chIndex++) {
            var ch = chapters[chIndex];
            var chData = drugGroupCosts[orgs[index]][ch];
            var value = chData != undefined ? chData[month] : undefined;
            costs.push(value != undefined ? value : null);
        }
        var trace = {
            x: chs,
            y: costs,
            name: orgs[index],
            type : 'bar'
        };
        traces.push(trace);
    }

    var data = traces;
    var layout = {
        title: 'Detailed costs for all the chapters for the focus group',
        xaxis: {
            title: 'BNF Chapter',
            tickangle: -45
        },
        yaxis: {
            title: 'Total Costs (in GBP)',
            zeroline: false,
            gridwidth: 2
        },
    };

    Plotly.newPlot('2DDetailedCostsDiv', data, layout);
}

// get drug group code
function getDrugGroupCode(groupName) {
    return drugGroupBnfMapping[groupName];
}

// update group costs plot
function updateGroupCostsPlot() {
    var traces = [];
    var orgs = getOrgs();
    var months = Object.keys(trend_dates);
    for (var dgIndex in drugGroupSelected) {
        var dgName = drugGroupSelected[dgIndex];
        var dg = getDrugGroupCode(dgName);
        for (var index = 0; index < orgs.length; index++) {
            var costs = [];
            for (var month in rev_trend_dates) {
                var value = drugGroupCosts[orgs[index]][dg][month];
                costs.push(value != undefined ? value : null);
            }
            var trace = {
                x: months,
                y: costs,
                mode: 'lines',
                name: orgs[index] + ' ' + dgName,
                line: {
                    dash: 'solid',
                    width: 4
                }
            };
            traces.push(trace);
        }
    }

    var data = traces;
    var layout = {
        title: 'Detailed costs for drug group: ' + drugGroupId,
        xaxis: {
            title: 'Month of the year',
            range: [0, 24],
            autorange: true
        },
        yaxis: {
            title: 'Total Costs (in GBP)',
            range: [0, 18.5],
            autorange: true
        },
        legend: {
            y: 0.5,
            traceorder: 'reversed',
            font: {
                size: 16
            }
        }
    };

    Plotly.newPlot('2DSubChapterCostsDiv', data, layout);
}

