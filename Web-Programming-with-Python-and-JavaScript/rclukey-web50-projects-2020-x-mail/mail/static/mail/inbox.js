document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email());

  document.querySelector("#compose-form").addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#mail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // List the emails on the webserver
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    console.log(emails);

    // ... do something else with emails ...
    emails.forEach(email => {
      const new_email = document.createElement('div');
      new_email.className = 'list-group-item';
      new_email.style.border = '1px solid black';
      new_email.style.margin = '2px';
      new_email.innerHTML = `
        <h4>From: ${email.sender}</h4>
        <h5>Subject: ${email.subject}</h5>
        <p>${email.timestamp}</p>`;
      new_email.className = email.read ? 'read' : 'not_ready';
      new_email.addEventListener('click', function() {
        console.log('This element has been clicked!')
        load_email(email.id, mailbox)
      });
      document.querySelector('#emails-view').append(new_email);
    });
  });
}

function send_email(event){
  event.preventDefault()

  // Retrieve the email from the webserver
  const recipient = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const body = document.querySelector("#compose-body").value;

  // Post the email to the API
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipient,
      subject: subject,
      body: body,
    })
  })
  .then(response => response.json())
  .then(result => {
    // Print result
    console.log(result);

    // Go to sent mail
    load_mailbox('sent');
  });
  
}

function load_email(id, mailbox) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'block';

  document.querySelector('#mail-view').innerHTML = '';

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    // Print email
    console.log(email);

    // ... do something else with email ...
    const new_email = document.createElement('div');
    new_email.className = 'list-group-item';
    new_email.innerHTML = 
      `<h4>From: ${email.sender}</h4>
      <h4>To: ${email.recipients}</h4>
      <h5>Subject: ${email.subject}</h5>
      <p>${email.timestamp}</p>
      <p>${email.body}</p>`;
    
    if (!email.read) {
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      })
    }

    document.querySelector('#mail-view').append(new_email);

    if (mailbox !== 'sent') {
      const archive = document.createElement('button');
      archive.innerHTML = email.archived ? "Unarchive" : "Archive";
      archive.addEventListener('click', () => {
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: !email.archived
          })
        })
        .then(() => {load_mailbox('inbox')})
      });
      document.querySelector('#mail-view').append(archive);
    }
    const reply = document.createElement('button');
    reply.innerHTML = "Reply";
    reply.addEventListener('click', () => {
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#mail-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'block';

      document.querySelector('#compose-recipients').value = email.sender;

      let subject = email.subject;
      if (subject.split(' ', 2)[0] !== "Re:") {
        subject = "Re: " + email.subject;
      }

      document.querySelector('#compose-subject').value = subject;
      document.querySelector('#compose-body').value = `
        On ${email.timestamp}, ${email.sender} wrote:
        ${email.body}
        `;
    });
    document.querySelector('#mail-view').append(reply);
  });
}

console