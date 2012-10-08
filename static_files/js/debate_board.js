/*
    debate_board.js - Javascript containing the engine for the debate
                           system.
                           
    License: GPLv3
    Copyright: 2011 Cidadania S. Coop. Galega
    Author: Oscar Carballal Prego <info@oscarcp.com>
*/
var newTitle = 'Наслов';
var newMessage = 'Овде напишија твојата порака';
var editString = 'Измени';
var viewString = 'види';
var errorMsg = 'Има некаква грешка.';
var errorCreate = "Мислењето не може да се креира.";
var errorGetNote = "Деталите од мислењето се недостапни.";
var errorSave = "Мислењето не може да се зачува.";
var errorSavePos = "Не може да се промени позицијата.";
var errorDelete = "Мислењето не може да се избрише.";
var confirmDelete = 'Дали сте сигурни?';


function showControls() {
    /*
     showControls() - Hides the edit and delete controls from the notes. If the
     users hovers over a note created by himself, the note shows the controls.
     */
    $(".mine").hover(function(){
            $(this).find(".deletenote").show();
            $(this).find("#edit-note").show();
            $(this).find("#view-note").show();
        },
        function() {
            $(this).find(".deletenote").hide();
            $(this).find("#edit-note").hide();
            $(this).find("#view-note").hide();
        }
    );
}

function editNote(obj) {
    /*
        editNote(obj) - This function detects the note the user clicked and raises
        a modal dialog, after that it checks the note in the server and returns
        it's data, prepopulating the fields.
    */
    var noteID = $(obj).parent().parent().attr('id');

    var request = $.ajax({
        url: "../update_note/",
        data: { noteid: noteID }
    });

    request.done(function(note) {

        $('#edit-current-note').modal('show');
        $("input[name='notename']").val(note.title);
        wysieditor.data("wysihtml5").editor.setValue(note.message, true);
        $("textarea#id_note_message").val(note.message);
        $("#last-edited-note").text(noteID);
    });

    request.fail(function (jqXHR, textStatus) {
        $('#edit-current-note').modal('hide');
        $('#jsnotify').notify("create", {
            title: errorGetNote,
            text: errorMsg + textStatus,
            icon:"alert.png"
        });
    });
}
function createNote() {
    /*
        createNote() - Creates a new note related with the debate. Frist the
        function creates the note in the server and after that we create a "fake"
        note in the debate board with the data returned by the view. If for some
        reason the user creates the note and leaves it before moving or editing the
        note is positioned in position [1,1].
    */

    var request = $.ajax({
        type:"POST",
        url:"../create_note/",
        data:{
            debateid:$('#debate-number').text(),
            title: newTitle,
            message: newMessage,
            column:$('#col').text(),
            row:$('#row').text()
        }
    });

    request.done(function (note) {
        var newNote = $("#sortable-debate").append("<div id='" + note.id + "' style='display:hidden;' class='note logged mine'>" +       "<div class='handler'><div class='deletenote hidden'>" + "<a href='#' onclick='deleteNote(this)'" +
            " id='deletenote'>x</a></div></div><p class='note-text'>" + note.title + "</p>" +
            "<span id='view-note' class='label hidden'><a href='?note=" + note.id + "' onclick='viewNote(this)' data-toggle='modal' data-target='#view-current-note'>" + viewString + "</a></span>" +
            "<span id='edit-note' class='label hidden'><a href='#' onclick='editNote(this)' data-toggle='modal' data-target='#edit-current-note'>" + editString + "</a></span></div>");
        var noteEditLink = $("#sortable-debate").find("#" + note.id).find("#edit-note").find('a');
        newNote.show('5000');
        showControls();
	editNote(noteEditLink);
    });

    request.fail(function (jqXHR, textStatus) {
        $('#jsnotify').notify("create", {
            title: errorCreate,
            text: errorMsg + textStatus,
            icon:"alert.png"
        });
    });

    // Activate control show/hide for the new note
}

function viewNote(obj) {
    var noteID = $(obj).parent().parent().attr('id');

    var request = $.ajax({
        url: "../update_note/",
        data: { noteid: noteID }
    });

    request.done(function(note) {
        $('h5#view-note-title').text(note.title);
        $('p#view-note-desc').html(note.message);
        $('span#view-note-author').text(note.author.name);
        var html = '';
        var buttons = '';
        var url = "http://republikamladi.mk/debate/"+ note.debate.id + "?note=" + noteID;
        buttons +=  "<a class='addthis_button_facebook_like' fb:like:layout='button_count'></a>";
        buttons +=  "<a class='addthis_button_tweet'></a>";
	buttons +=  "<meta property='og:title' content='" + note.title +"' /><meta property='og:description' content='" + note.message +"' />" ; 
        buttons +=  "<a class='addthis_button_facebook_share' fb:share:layout='button_count'></a>";
        var script = "<script type='text/javascript' src='http://s7.addthis.com/js/250/addthis_widget.js#pubid=ra-4ff2f3a930eacab9'></script>";
        var comment_count = "<h5 class='note-comment-title'>Коментари (" + note.comments.length + ")";
	for(var i=0; i<note.comments.length; i++) {
            var item = note.comments[i];
	    html += "<div class='comment-bubble' id='comment" + i +"'>" + "<p id='username' class='viewer'>" + item.username + "</p>";
	    html += "<p id='date' class='viewer-date'>"+ item.submit_date +"</p>";
	    html += "<p id='comments" + i + "' class='viewer-comment'>" + item.comment + "</p><img src='/static/img/images/arrow-2.png' width='20' height='21'></div>";
}
        var tweet_text = note.title + '- Дебатирај на @republikamladi #mladimk';
        $('div#comments').html(html);
        $('span#num-comments').html(comment_count);
        $('form#form_comments div.kopce').html(note.form_html);
        $('div#something').attr('addthis:url', url);
        $('div#something').attr('addthis:title', tweet_text);
        $('div#something').attr('addthis:description', note.message);
        $('div#buttons').html(buttons);
        if (window.addthis){ window.addthis = null; }
        $.getScript('http://s7.addthis.com/js/250/addthis_widget.js#pubid=ra-4ff2f3a930eacab9&async=1',
    function(){
        addthis.init(); //callback function for script loading
    });  

});
    request.fail(function (jqXHR, textStatus) {
        $('#edit-current-note').modal('hide');
        $('#jsnotify').notify("create", {
            title: errorGetNote,
            text: errorMsg + textStatus,
            icon:"alert.png"
        });
    });
	return false;
}


function saveNote() {
    /*
        saveNote() - Saves the current edited note, only the title and message
        field, since the other fields are managed through makeSortable() or by
        django itself.
    */
    var noteID = $('#last-edited-note').text();

    var request = $.ajax({
        type: "POST",
        url: "../update_note/",
        data: {
            noteid: noteID,
            title: $("input[name='notename']").val(),
            message: $("textarea#id_note_message").val()
//            message: $("td#cke_contents_id_note_message .cke_show_borders").text()
        }
    });

    request.done(function(msg) {
        $('#edit-current-note').modal('hide');
        var newTitle = $("input[name='notename']").val();
        $("div#" + noteID + " > p").text(newTitle);
        location.reload();
    });

    request.fail(function(jqXHR, textStatus) {
        $('#edit-current-note').modal('hide');
        $('#jsnotify').notify("create", {
            title: errorSave,
            text: errorMsg + textStatus,
            icon:"alert.png"
        });
    })
}

function deleteNote(obj) {
    /*
        deleteNote() - Delete a note making an AJAX call. This function is called
        through getClickedNote(). We locate the note ID, and post it to django,
        after that we hide the note from the board and when it's hidden we remove it
        from the DOM.
    */
    var noteID = $(obj).parents('.note').attr('id');
    var answer = confirm(confirmDelete);

    if (answer) {
        var request = $.ajax({
            type: "POST",
            url: "../delete_note/",
            data: { noteid: noteID }
        });

        request.done(function(msg) {
           $('#' + noteID).hide("normal", function() {
               $('#' + noteID).remove();
           });
        });

        request.fail(function(jqXHR, textStatus) {
            $('#jsnotify').notify("create", {
                title: errorDelete,
                text: errorMsg + textStatus,
                icon:"alert.png"
            });
        });
    }
}
function makeSortable() {
    /*
        makeSortable() - Makes every element with id starting by 'sortable'
        sortable through the connectedSortable class lists. It uses jQuery
        Sortable. This function has to be called whenever a new element is on
        the page (note, table column or row) to make the new elements sortable.
    */
    
    // Get all the div elements starting by sortable
    $('#[id^=sortable]').sortable({
        connectWith: ".connectedSortable",
    	cursor: "move",
    	placeholder: "note-alpha",
    	start: function(e,ui) { 
            $(ui.placeholder).hide("slow"); // Remove popping
        },
        change: function(e,ui) {
            $(ui.placeholder).hide().show("normal");
        },
        stop: function(e,ui) {
            var noteObj = ui.item;
            var noteID = noteObj.attr('id');
            var position = noteObj.parent().attr('headers').split("-");

            $.ajax({
                type: "POST",
                url: "../update_position/",
                data: {
                    noteid: noteID,
                    column: position[0],
                    row: position[1]
                }
            }).fail(function(jqXHR, textStatus) {
                $('#jsnotify').notify("create", {
                    title: errorSavePos,
                    text: errorMsg + textStatus,
                    icon:"alert.png"
                });
            });
        }
    }).disableSelection();
}

/* DEBATE CREATION */

var tdlength = 0;

function addTableColumn() {
    /*
        addTableColumn() - Create a new column ny creating a new sortable TD in
        all the rows.
    */
    var tableID = $('table').attr('id');
    var inputs = $('#' + tableID + ' input').length;
    var tdlength = $('#' + tableID + ' td').length;
    var criteriacount = $('#' + tableID + ' th[id^=debate-vcriteria]').length;
    var formCount = parseInt($('#id_colform-TOTAL_FORMS').val());

    if (criteriacount >= 10) return false;
    $('#' + tableID + ' tr:first').append("<th id='debate-vcriteria" + (criteriacount+1) + "' class='criteria-vtitle'><input id='" + tableID + "-criteria" + (inputs+1) + "' name='colform-" + (criteriacount) + "-criteria' type='text' class='small' value='Test criteria'></th>");
    $('#' + tableID + ' tbody tr').each(function(){
        //var tdlength = $('#' + tableID + ' td').length;
        $(this).append("<td id='sortable" + (tdlength) + "-" + tableID + "' class='connectedSortable'></td>").fadeIn("slow");
        tdlength += 1;
    });
    $('#id_colform-TOTAL_FORMS').val(formCount + 1);
    makeSortable();
}

function addTableRow() {
    var tableID =$('table').attr('id');
    var criteriacount = $('#' + tableID + ' th[id^=debate-vcriteria]').length;
    var tdlength = $('#' + tableID + 'td').length;
    var formCount_row = parseInt($('#id_rowform-TOTAL_FORMS').val());

    var t = $('table');
    var numColumns = $('th[id^=debate-vcriteria]', t).length;
    var numRows = $('td[class=criteria-htitle]', t).length;
    if (numRows >= 10) return false;

    var tr = $('<tr>');
    tr.append("<td class='criteria-htitle'><div id='debate-ttitle'><input id='" + tableID + "-criteria" + (numRows) + "' name='rowform-" + (numRows) + "-criteria' type='text'></div></td>");
    $('#id_rowform-TOTAL_FORMS').val(formCount_row + 1);
    for (i=0; i<numColumns; i++) {
        tr.append('<td>');
    }
    t.append(tr);

}

function removeTableRow() {
    var t = $('table');
    var numRows = $('td[class=criteria-htitle]', t).length;
    var formCount_row = parseInt($('#id_rowform-TOTAL_FORMS').val());
    if (numRows < 2) return false;
    $('tbody tr:last-child').fadeOut("fast", function() {
        $(this).remove();
    $('#id_rowform-TOTAL_FORMS').val(formCount_row - 1);

    });

}

function removeTableColumn() {
    /*
        removeTableColumn() - Deletes the last column (all the last TDs).
    */
    var tableID = $('table').attr('id');
    var formCount = parseInt($('#id_colform-TOTAL_FORMS').val());
    var columns = $('#' + tableID+ ' tr:last td').length;
    if (columns > 2) {
        $('#' + tableID + ' th:last-child, #' + tableID + ' td:last-child').fadeOut("fast", function() {
            $(this).remove();
        $('#id_colform-TOTAL_FORMS').val(formCount - 1);

        });
    } 
    else {
        $('#jsnotify').notify("create", {
            title: "Can't delete column",
            text: "There must be at least one column in the table.",
            icon: "alert.png"
        });
    }
}

function saveTable() {
    /*
        saveTable() - Saves the table data. Instead of using a standard form,
        we submite the data trough ajax post, and treat it as a form in the
        django view.
    */
    $('#ajaxform').submit( function(e) {
        var tableID = $('table').attr('id');

        var xvalues = [];
      //  var xfields = $('th.criteria-vtitle :input');
      //  $.each(xfields, function(i, field){
      //      xvalues.push(field.value);
      //  });
        $('#id_columns').val(xvalues);
        var sortable = [];
        var rows = $('#' + tableID + ' tbody tr');
        $.each(rows, function(i, field) {
            var rowID = this.attr('id');
            $(rowID + ' td').each(function() {
                sortable.push($(this).attr('id'));
            })
    //        alert('Estos son los sortables: ' + sortable[0]);
            $(this).val(sortable);
            sortable.length = 0;
        });
    });
}

/*******************
    MAIN LOOP
********************/

$(document).ready(function() {
    // Activate javascript notifications.
    $('#jsnotify').notify();
    // Activate sortables
    makeSortable();
    // Show controls for some notes
    showControls();
    saveTable();
});

