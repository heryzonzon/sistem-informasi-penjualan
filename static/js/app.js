var url = window.location.href;

var addHighlightClass = [
    { 'url': '/items', 'class': 'item' },
    { 'url': '/suppliers', 'class': 'supplier' },
    { 'url': '/customers', 'class': 'customer' },
    { 'url': '/invoices/purchase', 'class': 'invoice_purchase' },
    { 'url': '/invoices/sales/', 'class': 'invoice_sales' },
    { 'url': '/transactions/purchase', 'class': 'transaction_purchase' },
    { 'url': '/transactions/sales/', 'class': 'transaction_sales' },
    { 'url': '/users', 'class': 'users' },
    { 'url': '/login', 'class': 'login' }
];

for ( var i = 0; i < addHighlightClass.length; i++ ) {
    var obj = addHighlightClass[i];

    if ( url.match( obj.url ) ) {
        var menu = document.getElementsByClassName(obj.class)[0];
        window.tes = menu;

        if ( menu ) {
            menu.className += ' active';
            break;
        }
    }
}

// select2
$('form select').select2();
$('.select2-container').css({ marginLeft: 0, paddingLeft: 0 });

// invoice detail
// TODO need fix bug below
var tableDetail = {
    show: function(el) {
        $(el).addClass('label label-info')
            .parents('tr')
            .next('tr')
            .fadeIn('fast');
    },
    hide: function(el) {
        $(el).removeClass('label label-info')
            .parents('tr')
            .next('tr')
            .fadeOut('fast');
    }
}

$('.table-detail').toggle(function() { // on state
    tableDetail.show(this);
}, function() { // off state
    tableDetail.hide(this);
});

$('.collapse-all').click(function() {
    $('.table-detail').each(function() {
        tableDetail.show(this);
    });
})

$('.hide-all').click(function() {
    $('.table-detail').each(function() {
        tableDetail.hide(this);
    });
})

// angularjs
var app = angular.module('TemanBan', ['ngResource', 'ui.highlight']);

app.config(function( $interpolateProvider ) {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
});

app.controller('Item', function( $scope, $resource ) {
    var resource = $resource('/api/items/:id', { id: '@id' }, {
        query: {
            method:'GET',
            isArray: false
        }
    });

    resource.query(function( res ) {
        $scope.data = res.data;
    });

    $scope.remove = function( id ) {
        resource.remove({ id: id }, function() {
            resource.query(function( res ) {
                $scope.data = res.data;
            });
        });
    }
});
