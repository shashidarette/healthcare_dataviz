// This is the java-script file with client logic specific for GP Profiles
var gpProfileData = [];

function updatePracticeInfo(parent, practiceCode) {
    var practiceData = gpProfileData[practiceCode];

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
                var group_id = '#focus_group_' + group_index + ' ';
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