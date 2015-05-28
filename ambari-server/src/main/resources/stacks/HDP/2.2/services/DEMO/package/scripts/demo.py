#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
import os
from ambari_commons import OSConst
from resource_management import *

#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import sys
from resource_management import *

class DEMO(Script):


    def install(self, env):
        #self.install_packages(env)
        print 'installed demo'

    def configure(self, env):
        print 'configured demo'

    def start(self, env):
        import os
        import params
        os.system(os.path.join(params.dse_server_home, 'start.sh'))
        File(os.path.join(params.dse_server_pid_dir, "demo.pid"),
             owner="ambari",
             content="290"
        )
        print 'start demo'

    def stop(self, env):
        import os
        import params
        os.system(os.path.join(params.dse_server_home, 'kill.sh'))
        os.remove(os.path.join(params.dse_server_pid_dir, "demo.pid"))
        print 'stop demo'

    def status(self, env):
        import os.path
        import params
        if not os.path.isfile(os.path.join(params.dse_server_pid_dir, "demo.pid")):
            raise ComponentIsNotRunning()
        pass

    def decommission(self, env):
        print 'decommission demo'


if __name__ == "__main__":
    DEMO().execute()

