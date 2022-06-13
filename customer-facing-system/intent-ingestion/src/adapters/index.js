// The adapters is where we add functions that interacts with the external world
// where in our case its implementing rest API
import * as authAdapters from './auth';

export default {
  ...authAdapters,
};
