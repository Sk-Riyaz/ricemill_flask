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
    $("form").not('#report')
        .$('select#variety, select#agent')
        .prepend($("<option></option>")
            .attr("value", "")
            .attr("selected", "")
            .text("Select"))

    $("#purchase #rate").change(function () {
        let rate = $("#rate").val();
        if (!rate) {
            $("#purchase #amount").attr("value", 0);
            return;
        }
        $("#purchase #amount").attr("value", rate);
    })

    $("#sale #quintol, #sale #rate").change(function () {
        let quintol = $("#quintol").val();
        let rate = $("#rate").val();
        if (!quintol || !rate) {
            $("#sale #amount").attr("value", 0);
            return;
        }
        $("#sale #amount").attr("value", updateSalesAmount(quintol, rate));
    })
})
