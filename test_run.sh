sudo -u postgres dropdb market_test
sudo -u postgres createdb market_test
sudo -u postgres psql market_test < market.psql