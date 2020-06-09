const uploading2 = document.getElementById("uploading2");
const error2 = document.getElementById("error2");
const uploaded2 = document.getElementById("uploaded2");
const audio = document.getElementById("audio");
const audioText = document.getElementById("audioText");
const table = document.getElementById("table");
const tableRef = table.getElementsByTagName('tbody')[0];

$(document).ready(function() {
    uploaded2.style.display = "none";
    error2.style.display = "none";
    uploading2.style.display = "none";

    audio.style.display = "none";
    audioText.style.display = "none";

    getDatabaseContents();
});

function isEmpty(el) {
    return !$.trim(el.html())
}

var count = 0;

var addSerialNumber = function() {
    $('table tr').each(function(index) {
        $(this).find('td:nth-child(1)').html(index);
    });
};

addSerialNumber();

$('#Upload').on('click', function() {
    uploading2.style.display = "block";
    if (isEmpty($('#myFiles'))) {
        uploading2.style.display = "none";
        error2.style.display = "block";
    } else {
        lang = $('input[name="langRadio"]:checked').val();
        let SttLang = {
            language: lang
        };

        formData = new FormData($('form')[0]);
        formData.append("SttLang", JSON.stringify(SttLang));

        error2.style.display = "none";
        $.ajax({
            url: '/uploader',
            type: 'POST',
            data: formData,
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false,
            success: function(myData) {
                uploading2.style.display = "none";

                audioPlayer = '<br/><a><audio controls> <source src="' +
                    myData.filepath + '" type="audio/wav"> Your browser does not support the audio element. </audio></a>';
                audio.innerHTML = audioPlayer;

                audio.style.display = "block";
                audioText.style.display = "block";

                getDatabaseContents();
            },
            error: function() {
                error2.style.display = "block";
            }
        });
    }

});

async function getDatabaseContents() {
    await fetch('/getDatabaseContents').then(async(response) => {
        $("table").find("tr:gt(0)").remove();
        data = await response.json();

        data.forEach(element => {
            var row = table.insertRow(1);

            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);
            var cell4 = row.insertCell(3);
            var cell5 = row.insertCell(4);
            var cell6 = row.insertCell(5);

            cell1.innerHTML = "";
            cell2.innerHTML = element.NAME;
            cell3.innerHTML = element.PHONE;
            cell4.innerHTML = element.ORDERS;
            cell5.innerHTML = element.ADDRESS;
            cell6.innerHTML = `<button class="bx--btn--small bx--btn--danger bx--btn--icon-only bx--tooltip__trigger bx--tooltip--a11y bx--tooltip--bottom bx--tooltip--align-center" onclick="remove(${element.ID})">
  <span class="bx--assistive-text">Remove</span>
  <svg focusable="false" preserveAspectRatio="xMidYMid meet" style="will-change: transform;" xmlns="http://www.w3.org/2000/svg" class="bx--btn__icon" width="16" height="16" viewBox="0 0 16 16" aria-hidden="true">
<path d="M11 4v11c0 .6-.4 1-1 1H2c-.6 0-1-.4-1-1V4H0V3h12v1h-1zM2 4v11h8V4H2z"></path><path d="M4 6h1v7H4zM7 6h1v7H7zM3 1V0h6v1z"></path></svg>
</button>`;

            addSerialNumber();
        });
    });
}

async function remove(ID) {
    await fetch(`/deleteRecord/${ID}`).then(async(response) => {
        data = await response.json();
        if (data.flag == 'success') {
            location.reload();
        }
    });
}