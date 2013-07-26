//var url = window.location.href;
//
//var addHighlightClass = [
//    { 'url': '/items', 'class': 'item' },
//    { 'url': '/suppliers', 'class': 'supplier' },
//    { 'url': '/customers', 'class': 'customer' },
//    { 'url': '/invoices/purchase', 'class': 'invoice_purchase' },
//    { 'url': '/invoices/sales/', 'class': 'invoice_sales' },
//    { 'url': '/transactions/purchase', 'class': 'transaction_purchase' },
//    { 'url': '/transactions/sales/', 'class': 'transaction_sales' },
//    { 'url': '/users', 'class': 'users' },
//    { 'url': '/login', 'class': 'login' }
//];
//
//for ( var i = 0; i < addHighlightClass.length; i++ ) {
//    var obj = addHighlightClass[i];
//
//    if ( url.match( obj.url ) ) {
//        var menu = document.getElementsByClassName(obj.class)[0];
//        window.tes = menu;
//
//        if ( menu ) {
//            menu.className += ' active';
//            break;
//        }
//    }
//}

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

app.config(function( $routeProvider, $locationProvider ) {
    $locationProvider.html5Mode(false).hashPrefix('!');
    $routeProvider
        /***********
         * ITEM
         **********/
        .when('/item', {
            templateUrl: '/template/item/list.html',
            controller: 'Item'
        })
        .when('/item/new', {
            templateUrl: '/template/item/new.html',
            controller: 'Item'
        })
        .when('/item/:itemId', {
            templateUrl: function( params ) {
                return '/template/item/edit.html'
            },
            controller: 'Item'
        })
        /***********
         * SUPPLIER
         **********/
        .when('/supplier', {
            templateUrl: '/template/supplier/list.html',
            controller: 'Supplier'
        })
        .when('/supplier/new', {
            templateUrl: '/template/supplier/new.html',
            controller: 'Supplier'
        })
        .when('/supplier/:supplierId', {
            templateUrl: function( params ) {
                return '/template/supplier/edit.html'
            },
            controller: 'Supplier'
        })
        /***********
         * CUSTOMER
         **********/
        .when('/customer', {
            templateUrl: '/template/customer/list.html',
            controller: 'Customer'
        })
        .when('/customer/new', {
            templateUrl: '/template/customer/new.html',
            controller: 'Customer'
        })
        .when('/customer/:customerId', {
            templateUrl: function( params ) {
                return '/template/customer/edit.html'
            },
            controller: 'Customer'
        })
        /***********
         * HOME
         **********/
        .otherwise({ redirectTo: '/' });
});

app.config(function( $interpolateProvider ) {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
});

app.filter('rupiah', function() {
    return function( string ) {
        if ( string ) {
            return accounting.formatMoney(parseInt(string), 'Rp ', '.', '.') + ',-';
        } else {
            return '-';
        }
    }
});

app.directive('activeLink', ['$location', function( location ) {
    return {
        restrict: 'A',
        link: function( scope, element, attrs, controller) {
            var path = element.children('a').attr('href').substring(3);
            scope.location = location;

            scope.$watch('location.path()', function( newPath ) {
                newPath = '/' + newPath.split('/')[1];

                if ( path == newPath ) {
                    element.addClass('active');
                } else {
                    element.removeClass('active');
                }
            })
        }
    };
}]);

/***********
 * ITEM
 **********/
app.controller('Item', function( $scope, $resource, $routeParams, $location ) {
    var resource = $resource('/api/items/:id', { id: '@id' }, {
        query: { method:'GET', isArray: false },
        update: { method: 'PUT' }
    });

    resource.query(function( res ) {
        $scope.data = res.data;
    });

    $scope.messages = {
        error: false,
        success: false
    };

    $scope.add = function() {
        resource.save($scope.item, function() {
            $scope.messages.success = true;
            $scope.item = {
                stock: 0,
                price_buy: 0,
                price_sell: 0
            };
            $('#barcode').focus();
        }, function( err ) {
            if ( err.status == 500 ) {
                $scope.messages.error = false;
            }
        });
    }

    $scope.load = function() {
        $scope.item = resource.get({ id: $routeParams.itemId })
    };

    $scope.update = function() {
        $scope.item.$update(function() {
            $location.path('/item')
        }, function( err ) {
            if ( err.status == 500 ) {
                $scope.messages.error = false;
            }
        });
    }

    $scope.remove = function( id ) {
        resource.remove({ id: id }, function() {
            resource.query(function( res ) {
                $scope.data = res.data;
            });
        });
    }
});


/***********
 * SUPPLIER
 **********/
app.controller('Supplier', function( $scope, $resource, $routeParams, $location ) {
    var resource = $resource('/api/suppliers/:id', { id: '@id' }, {
        query: { method:'GET', isArray: false },
        update: { method: 'PUT' }
    });

    resource.query(function( res ) {
        $scope.data = res.data;
    });

    $scope.messages = {
        error: false,
        success: false
    };

    $scope.add = function() {
        resource.save($scope.supplier, function() {
            $scope.messages.success = true;
            $scope.supplier = {};
            $('#name').focus();
        }, function( err ) {
            if ( err.status == 500 ) {
                $scope.messages.error = false;
            }
        });
    }

    $scope.load = function() {
        $scope.supplier = resource.get({ id: $routeParams.supplierId })
    };

    $scope.update = function() {
        $scope.supplier.$update(function() {
            $location.path('/supplier')
        }, function( err ) {
            if ( err.status == 500 ) {
                $scope.messages.error = false;
            }
        });
    }

    $scope.remove = function( id ) {
        resource.remove({ id: id }, function() {
            resource.query(function( res ) {
                $scope.data = res.data;
            });
        });
    }
});

/***********
 * CUSTOMER
 **********/
app.controller('Customer', function( $scope, $resource, $routeParams, $location ) {
    var resource = $resource('/api/customers/:id', { id: '@id' }, {
        query: { method:'GET', isArray: false },
        update: { method: 'PUT' }
    });

    resource.query(function( res ) {
        $scope.data = res.data;
    });

    $scope.messages = {
        error: false,
        success: false
    };

    $scope.add = function() {
        resource.save($scope.customer, function() {
            $scope.messages.success = true;
            $scope.customer = {};
            $('#name').focus();
        }, function( err ) {
            if ( err.status == 500 ) {
                $scope.messages.error = false;
            }
        });
    }

    $scope.load = function() {
        $scope.customer = resource.get({ id: $routeParams.customerId })
    };

    $scope.update = function() {
        $scope.customer.$update(function() {
            $location.path('/customer')
        }, function( err ) {
            if ( err.status == 500 ) {
                $scope.messages.error = false;
            }
        });
    }

    $scope.remove = function( id ) {
        resource.remove({ id: id }, function() {
            resource.query(function( res ) {
                $scope.data = res.data;
            });
        });
    }
});
