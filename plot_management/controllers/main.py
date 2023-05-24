from odoo import http
from odoo.http import request


class Plot(http.Controller):

    @http.route('/plot_management/customer', auth='public', website=True)
    def plot_record(self):
        # return "haii"

        customer = request.env['plot.customer'].sudo().search([])
        print("customer--",customer)
        return request.render("plot_management.plot_page", {
            'customer': customer
        })

    # @http.route('/get_customer', type='json', auth='user')
    # def get_patients(self):
    #     print("Yes here entered")
    #     customer = request.env['res.users'].search(['name','=',"Administrator"])
        # patients = []
        # for rec in customer:
        #     vals = {
        #
        #         'name': rec.name,
        #
        #     }
        #     customer.append(vals)
        # print("customer List--->", customer)

        # data = {'status': 200, 'response': customer, 'message': 'Done All Patients Returned'}
        # return data




    @http.route('/get_customer', type='json', auth='user')
    def get_customer(self):
        print("Yes here entered")
        customers_rec = request.env['plot.customer'].search([])
        customers = []
        for rec in customers_rec:
            vals = {

                'name': rec.name,
                'photo': rec['photo']

            }
            customers.append(vals)
        print("Customer List--->", customers)
        data = {'status': 200, 'response': customers, 'message': 'Done All customer Returned'}
        return data



    @http.route('/create_customer', type='json', auth='user')
    def create_customer(self, **rec):
        if request.jsonrequest:
            print("rec", rec)
            if rec['name']:
                vals = {
                    'name': rec['name'],
                    # 'photo': rec['photo']
                }
                new_customer = request.env['plot.customer'].sudo().create(vals)
                print("New Customer Is", new_customer)
                args = {'success': True, 'message': 'Success', 'id': new_customer.id}
        return args
