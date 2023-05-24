odoo.define('warranty_registration_portal.portal', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
const Dialog = require('web.Dialog');
const {_t, qweb} = require('web.core');
const ajax = require('web.ajax');

publicWidget.registry.portalDetails = publicWidget.Widget.extend({
//                    $(document).ready(function() {
//                                      alert('hlooo')
//                                   $('.btn.btn-primary.warranty').hide();
//
//                                    });
    handleOnClick: function () {
         if($("#checking").is(':checked'))
                                    {

                                    $('.btn.btn-primary.warranty').show();


                                    }
                                    else
                                    {

                                    $('.btn.btn-primary.warranty').hide();

                                    }
    },
});



});
