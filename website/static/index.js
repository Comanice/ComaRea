function deleteNote(noteId){
    console.log("Deleting note with ID:", noteId);
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId }), // Use noteId here
    }).then((_res) => {
        window.location.href = "/feedback";
    });
}