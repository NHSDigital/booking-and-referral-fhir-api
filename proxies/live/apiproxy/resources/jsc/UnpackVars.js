// LEGACY: Copy the S3 routing table content into a named context variable.
// TO BE REMOVED together with the LegacyS3Routing flow in bref-target.xml.

var bookingReferralConfig = context.getVariable("targets");
context.setVariable("booking-and-referral-config", bookingReferralConfig)
