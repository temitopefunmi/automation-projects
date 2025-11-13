const vader = require('vader-sentiment');

module.exports = async function (context, req) {
  context.log('HTTP trigger function processed a request.');

  const text = (req.body && req.body.text);

  if (!text) {
    context.res = {
      status: 400,
      body: "Please pass a 'text' property in the request body."
    };
    return;
  }

  const intensity = 
vader.SentimentIntensityAnalyzer.polarity_scores(text);

  let sentiment = 'neutral';
  if (intensity.compound >= 0.05) {
    sentiment = 'positive';
  } else if (intensity.compound <= -0.05) {
    sentiment = 'negative';
  }

  context.res = {
    body: {
      sentiment: sentiment,
      score: intensity.compound
    }
  };
};
