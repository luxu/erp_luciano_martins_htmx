$(document).ready(function() {
    $('#id_name').autocomplete({
        delay: 600,
        minLength: 2,
        autoFocus: true,
        position: {
            my: 'left top',
            at: 'right top'
        },
        appendTo: "#form",
        source: function (request, response) {
            $.ajax({
                url: '/gasto/autocomplete/',
                type: 'get',
                dataType: 'html',
                data: {
                    'term': request.term
                }
            }).done(function (data) {
                if (data.length > 0) {
                    data = data.split(',')
                    response($.each(data, function (key, item) {
                        console.log(item)
                        return ({
                            label: item
                        });
                    }));
                }
            });
        }
    });

    $('#id_parcelas_gasto-0-valor_parcela').mask('000.000.000.000.000,00', {reverse: true});

    $('#id_parcelas_gasto-0-numero_parcela').on(
        "focusout", function() {
            const parcelas = $('#id_parcelas_gasto-0-numero_parcela').val();
            let add_one_month = '';
            let nro = 0;
            let nro_parcela = $('#id_parcelas_gasto-0-numero_parcela');
            nro_parcela.prop("readonly", true);
            $('#id_parcelas_gasto-0-valor_parcela').focus();
            const data_parcela = $('#id_parcelas_gasto-0-data_parcela');
            // const data_gasto = new Date($('#id_datagasto').val())

            const data_gasto = $('#id_datagasto').val();
            const day = data_gasto.split('/')[0];
            const month_current = data_gasto.split('/')[1];
            const year = data_gasto.split('/')[2];

            const dataEUA = year + '-' + month_current + '-' + day
            let dataAtual = new Date(dataEUA);

            let umMesDepois = new Date(dataAtual.getFullYear(), dataAtual.getMonth() + 1, dataAtual.getDate());

            // const convert_to_date = new Date(dia + '-' + mes + '-' + ano);

            let next_data = new Date(umMesDepois);
            // next_data.setMonth(data_gasto.getMonth() + 1);
            data_parcela.val(next_data.toISOString().split('T')[0])
        }
    );
});
