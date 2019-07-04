(function() {
    'use strict';
    window.addEventListener('load', function() {
      // Fetch all the forms we want to apply custom Bootstrap validation styles to
      let forms = document.getElementsByClassName('needs-validation');
      // Loop over them and prevent submission
      let validation = Array.prototype.filter.call(forms, function(form) {
        form.addEventListener('submit', function(event) {
          if (form.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
          }
          form.classList.add('was-validated');
        }, false);
      });
    }, false);
  })();


(function() {
    window.addEventListener('load', function() {
      let formName = document.getElementsByTagName("form");
      if (formName.length > 0 && formName[0].classList.contains("submitted")) {
         return false;
      }
      let varsel = document.getElementById('variety');
      if(varsel){

      // create new option element
      let opt = document.createElement('option');

      // create text node to add to option element (opt)
      opt.appendChild( document.createTextNode('Select') );

      // set value property of opt
      opt.value = '';

      // add opt to end of select box (sel)

        varsel.prepend(opt);
      varsel.options[0].selected = true;
      }
      


      let agentsel = document.getElementById('agent');
      if(agentsel){
      let agentopt = document.createElement('option');

      // create text node to add to option element (opt)
      agentopt.appendChild( document.createTextNode('Select') );

      // set value property of opt
      agentopt.value = '';

      agentsel.prepend(agentopt);
      agentsel.options[0].selected = true;
      }
    });
  }) ();

function updatePurchaseAmount() {
    let rate = document.getElementById("rate");

    let amt = document.getElementById('amount');
    amt.value = rate.value;
    return true;
};

function updateSalesAmount() {
    let rate = document.getElementById('rate');
    let quintol = document.getElementById('quintol');
    let gst = 5;

    let amt = document.getElementById('amount');
    amt.value = (quintol.value * rate.value) + (quintol.value * rate.value * gst / 100);
    return true;
};

function changeaction( ) {
    //document.updateForm.action += document.submitname.split(":")[1];
    alert("updateaction");
}

function getConfirmation() {
    changeaction( );
    /*
    {% if action != "delete" %}
        return true;
    {% endif %}
    let userName = document.submitname;
    let retVal = confirm("Do you want to delete [" +userName.split(":")[1] +"]?");
    if( retVal == true ) {
        document.updateForm.user.value = userName.split(":")[0];
        let chagedVal = document.updateForm.user.value;
        return true;
    }
    else {
        return false;
    }
    */
}
