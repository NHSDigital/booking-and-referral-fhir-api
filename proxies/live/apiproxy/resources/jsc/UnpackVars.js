var bookingReferralConfigRaw =  JSON.parse(context.getVariable("targets"));
var bookingReferralConfig = bookingReferralConfigRaw.content

context.setVariable("booking-and-referral-config", bookingReferralConfig)