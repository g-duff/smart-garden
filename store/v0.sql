CREATE TABLE IF NOT EXISTS location (
	id INTEGER PRIMARY KEY,
	"timestamp" TEXT NOT NULL,
	name TEXT NOT NULL,
	humidity REAL,
   	temperature REAL
);

CREATE TABLE IF NOT EXISTS plant (
	id INTEGER PRIMARY KEY,
	"timestamp" TEXT NOT NULL,
	name TEXT NOT NULL,
   	moisture_percent REAL,
	moisture_voltage REAL
)
