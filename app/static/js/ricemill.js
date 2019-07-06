(function () {
    'use strict';
    window.addEventListener('load', function () {
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        let forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        let validation = Array.prototype.filter.call(forms, function (form) {
            form.addEventListener('submit', function (event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();


(function () {
    window.addEventListener('load', function () {
        let formName = document.getElementsByTagName("form");
        if (formName.length > 0 && formName[0].classList.contains("submitted")) {
            return false;
        }
        let varsel = document.getElementById('variety');
        if (varsel) {
            // create new option element
            let opt = document.createElement('option');

            // create text node to add to option element (opt)
            opt.appendChild(document.createTextNode('Select'));

            // set value property of opt
            opt.value = '';

            // add opt to end of select box (sel)
            varsel.prepend(opt);
            varsel.options[0].selected = true;
        }

        let agentsel = document.getElementById('agent');
        if (agentsel) {
            // create new option element
            let agentopt = document.createElement('option');

            // create text node to add to option element (opt)
            agentopt.appendChild(document.createTextNode('Select'));

            // set value property of opt
            agentopt.value = '';

            agentsel.prepend(agentopt);
            agentsel.options[0].selected = true;
        }
    });
})();

function updatePurchaseAmount() {
    let rate = document.getElementById("rate");

    let amt = document.getElementById('amount');
    amt.value = rate.value;
    return true;
};

function updateSalesAmount(quintol, rate) {
    quintol = parseFloat(quintol);
    rate = parseFloat(rate);
    let gst = 5;
    return (quintol * rate) + (quintol * rate * gst / 100);
};


$(document).ready(function () {
    $("#sale #quintol").change(function () {
        let rate = $("#rate").val();
        if (!rate) {
            // console.log("rate is undefined", $("#quintol").val());
            return;
        }
        // console.log(this.value, rate);
        $("#sale #amount").value(updateSalesAmount(this.value, rate));
    })
})

$(document).ready(function () {
    $("#sale #rate").change(function () {
        let quintol = $("#quintol").val();
        if (!quintol) {
            // console.log("quintol is undefined", $("#rate").val());
            return;
        }
        // console.log(quintol, this.value);
        $("#sale #amount").attr("value", updateSalesAmount(quintol, this.value));
    })
})
