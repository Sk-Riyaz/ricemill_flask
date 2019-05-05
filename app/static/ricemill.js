(function() {
    'use strict';
    window.addEventListener('load', function() {
      // Fetch all the forms we want to apply custom Bootstrap validation styles to
      var forms = document.getElementsByClassName('needs-validation');
      // Loop over them and prevent submission
      var validation = Array.prototype.filter.call(forms, function(form) {
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
      var varsel = document.getElementById('variety');

      // create new option element
      var opt = document.createElement('option');

      // create text node to add to option element (opt)
      opt.appendChild( document.createTextNode('Select') );

      // set value property of opt
      opt.value = '';

      // add opt to end of select box (sel)
      varsel.prepend(opt);
      varsel.options[0].selected = true;


      var agentsel = document.getElementById('agent');
      var agentopt = document.createElement('option');

      // create text node to add to option element (opt)
      agentopt.appendChild( document.createTextNode('Select') );

      // set value property of opt
      agentopt.value = '';

      agentsel.prepend(agentopt);
      agentsel.options[0].selected = true;
    });
  }) ();

function updatePurchaseAmount() {
    var rate = document.getElementById("rate");

    var amt = document.getElementById('amount');
    amt.value = rate.value;
    return true;
};

function updateSalesAmount() {
    var rate = document.getElementById('rate');
    var quintol = document.getElementById('quintol');
    var gst = 5;

    var amt = document.getElementById('amount');
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
    var userName = document.submitname;
    var retVal = confirm("Do you want to delete [" +userName.split(":")[1] +"]?");
    if( retVal == true ) {
        document.updateForm.user.value = userName.split(":")[0];
        var chagedVal = document.updateForm.user.value;
        return true;
    }
    else {
        return false;
    }
    */
}