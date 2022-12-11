require "uri"
require "json"
require "net/http"

class Payment
    attr_accessor :code, :status, :concept, :institution
    def initialize(code, status, concept, institution)
        @code = code
        @status = status
        @concept = concept
        @institution = institution
     end
end

class PaymentController < ApplicationController

    def student
        
    end

    def registrar_pago

    end

    def status
        url = URI("http://localhost:3001/payments_request")
        http = Net::HTTP.new(url.host, url.port);
        request = Net::HTTP::Get.new(url)
        request["Content-Type"] = "application/json"
        request.body = JSON.dump({
        "code": params["code"]
        })

        @response = http.request(request)
        @response = JSON.parse(@response.body)
        @payment_list = Array.new
        @response.each do |payment|
            my_payment = Payment.new(payment["code"],
            payment["status"],
            payment["concept"],
            payment["institution"])
            @payment_list.push(my_payment)
        end
    end

    def test
        redirect_to "/payment_status/#{params["code"]}"
    end
end
