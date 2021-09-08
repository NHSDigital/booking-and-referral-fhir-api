
var bookingReferralConfig =  JSON.parse(context.getVariable("ServiceCallout.response"));
set_variables("booking-and-referral-config", bookingReferralConfig)
