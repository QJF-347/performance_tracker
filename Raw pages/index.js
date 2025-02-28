const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            // Prevent default link behavior (if needed)
            event.preventDefault();

            // Remove show-side-boarder from all links
            navLinks.forEach(navLink => {
                navLink.classList.remove('show-side-boarder');
            });

            // Add show-side-boarder to the clicked link
            link.classList.add('show-side-boarder');
        });
    });
document.getElementById('results').addEventListener('change', function() {
    const selectedYear = this.value;
  
    // Hide all term selects
    document.getElementById('term_year_1').style.display = 'none';
    document.getElementById('term_year_2').style.display = 'none';
    document.getElementById('term_year_3').style.display = 'none';
    document.getElementById('term_year_4').style.display = 'none';
  
    // Show the selected term select
    if (selectedYear) {
      const termSelectId = 'term_' + selectedYear;
      document.getElementById(termSelectId).style.display = 'inline-block';
    }
  });
 
  const botIcon = document.querySelector('.bot_icon');
  const chatBox = document.querySelector('.chat_box');
  const bot_close = document.querySelector("#bot_close");
  

  botIcon.addEventListener('click', function() {
      chatBox.classList.toggle('chat-box-open');
      botIcon.classList.add("hide-icon");

  });
  bot_close.addEventListener("click", ()=>{
    botIcon.classList.remove("hide-icon");
    chatBox.classList.remove("chat-box-open");
  });
