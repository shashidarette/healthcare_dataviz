// This is the java-script file with client logic specific for GP Profiles
var gpProfileData = [];

function updatePracticeInfo(parent, practiceCode) {
    var practiceData = gpProfileData[practiceCode];

    if (parent != '') {
        parent = '#' + parent + ' ';
    }
    updateAgeDistribution(parent, practiceData);
    updateHealthIndicators(parent, practiceData);
    $(parent + '#practice_code').text(practiceCode);
    $(parent + '#name').text(practiceData['Practice Name']);
    $(parent + '#areacode').text(practiceData['Area Team Code'] + ' ' + practiceData['PCO Name']);
    $(parent + '#avgage').text(practiceData['AvgAgeProfile']);
    $(parent + '#avg65age').text(practiceData['% aged 65+ years']);
    $(parent + '#pcount').text(practiceData['Diabetes: QOF prevalence (17+)']);
    $(parent + '#imd').text(practiceData['Deprivation score (IMD 2015)']);
    $(parent + '#totalSize').text(practiceData['TotalSize']);
    $(parent + '#hypPCount').text(practiceData['Hypertension: QOF prevalence (all ages)']);
    
}

// to plot age distibution
var ageDataColumns = ['Male 0-4', 'Female 0-4', 'Male 5-14', 'Female 5-14', 'Male 15-24', 'Female 15-24',
    'Male 25-34', 'Female 25-34', 'Male 35-44', 'Female 35-44', 'Male 45-54', 'Female 45-54',
    'Male 55-64', 'Female 55-64', 'Male 65-74', 'Female 65-74', 'Male 75+', 'Female 75+'];

var ageColors = ['rgb(0, 204, 0)',
                 'rgb(255, 255, 0)',
                 'rgb(118, 17, 195)',
                 'rgb(0, 48, 240)',
                 'rgb(240, 88, 0)',
                 'rgb(215, 11, 11)',
                 'rgb(11, 133, 215)',
                 'rgb(177, 180, 34)',
                 'rgb(255, 87, 51)',
                 'rgb(255, 0, 255)'
                    ];

var ageColumns = ['0-4', '5-14', '15-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75+'];
var genderColumnsColumns = ['Male', 'Female'];

// get values for practice based on age distribution
function getAgeValues(practiceData) {
    var agevalues = [];

    for (var index = 0; index < ageDataColumns.length; index += 2) {
        var maleCol = ageDataColumns[index];
        var femaleCol = ageDataColumns[index + 1];
        var ageSum = practiceData[maleCol] + practiceData[femaleCol]
        agevalues.push(ageSum);
    }

    return agevalues;
}

// get values based on gender distribution
function getGenderValues(practiceData) {
    var maleCount = 0;
    var femaleCount = 0;

    for (var index = 0; index < ageDataColumns.length; index += 2) {
        var maleCol = ageDataColumns[index];
        var femaleCol = ageDataColumns[index + 1];
        maleCount += practiceData[maleCol];
        femaleCount += practiceData[femaleCol]
    }

    var totalSize = practiceData['TotalSize'];
    var malePerc = (maleCount/totalSize) * 100;
    var femalePerc = (femaleCount/totalSize) * 100;

    return [malePerc, femalePerc];
}

// update age distribution plot
function updateAgeDistribution(parent, practiceData) {
    var data = [{
        values: getAgeValues(practiceData),
        labels: ageColumns,
        'marker': {'colors': ageColors },
        domain: {
            x: [0, 100]
        },
        hoverinfo: 'label+percent',
        type: 'pie'
    }]

    var layout = {
        title: 'GP Patient Age Distribution',
        showlegend: true,
        legend: {"orientation": "h"}
    };

    var ageDistelement = $(parent + '#age_demographic').get(0);

    if (ageDistelement != undefined) {
        Plotly.newPlot(ageDistelement, data, layout);
    }
}

// health indicators array
var thetaArray = ['AvgAgeProfile', '% aged 65+ years', '% of Diabetes patients',
    '% of Hypertension patients', 'Deprivation score (IMD 2015)', '% of Male', '% of Female', 'AvgAgeProfile'];

// health indicators
function getHealthIndicators(practiceData) {
    var healthIndicators = [];

    for (var index = 0; index < thetaArray.length - 3; index++) {
        var col = thetaArray[index];
        healthIndicators.push(practiceData[col]);
    }

    var gendPec = getGenderValues(practiceData);
    healthIndicators.push(gendPec[0]);
    healthIndicators.push(gendPec[1]);

    return healthIndicators;
}

// update health indicators plot
function updateHealthIndicators(parent, practiceData) {
    data = [{
        type: 'scatterpolar',
        r: getHealthIndicators(practiceData),
        theta: thetaArray,
        fill: 'toself'
    }]

    layout = {
        title: 'GP Health Indicators',
        polar: {
            radialaxis: {
                visible: true,
                range: [0, 60]
            }
        },
        showlegend: false,
    }
    var healthIndiElement = $(parent + '#health_indicators').get(0);

    if (healthIndiElement != undefined) {
        Plotly.plot(healthIndiElement, data, layout);
    }
}

// update GP Profile information
function updateGPProfile(focusGroup) {
    if (focusGroup != undefined) {
        var count = focusGroup.length;
        if (count == 1) {
            var practiceCode = focusGroup[0];
            updatePracticeInfo('', practiceCode);
        } else {
            // only 4 are considered
            for (var index = 0; index < 4; index++) {
                var practiceCode = focusGroup[index];
                var practiceData = gpProfileData[practiceCode];
                var group_index = index+1;
                var group_id = 'focus_group_' + group_index;
                updatePracticeInfo(group_id, practiceCode);
            }
        }
    }
}

// load GP Profiles from JSON
function loadGPProfiles() {
    if (gpProfileData.length == 0) {
        $.getJSON('./gpProfiles.json', function (data) {
            gpProfileData = data;
            updateGPProfile(focusGroup);
        })
    }
}