function deleteNote(noteID){
    fetch('/delete-note', {
      method: 'POST', 
      body: JSON.stringify({ noteID: noteID})
    }).then((_res)=>{
      window.location.href = "/";
    })
  }

    // Function to save scroll position to session storage
    function saveScrollPosition() {
        sessionStorage.setItem('scrollPosition', window.scrollY);
    }

    // Function to restore scroll position from session storage
    function restoreScrollPosition() {
        var scrollPosition = sessionStorage.getItem('scrollPosition');
        if (scrollPosition !== null) {
            window.scrollTo(0, parseInt(scrollPosition));
        }
    }

    // Save scroll position before reload
    window.addEventListener('beforeunload', saveScrollPosition);

    // Restore scroll position after reload
    window.addEventListener('load', restoreScrollPosition);