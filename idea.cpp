/*
    class
        void startPollingCoordinates(int pollInterval = 500) {
            interval = self.setInterval(() => {
                world.getAllActors();
                world.getAllPositions();
                // filter out relevant positions [later?]
                _addCoordinatesDeviation();
                saveCoordinates();
            }, pollInterval)
        }

        void stopPollingCoordinates() {
            clearInterval(interval);
        }
        
        Vector3D getActorPosition(int id) {}
        Map<int, Vector3D> getAllActorsPositions()
*/