# This file is part of GridCal.
#
# GridCal is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GridCal is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GridCal.  If not, see <http://www.gnu.org/licenses/>.
import os
import numpy as np

from GridCal.Engine import *
from tests.zip_file_mgmt import open_data_frame_from_zip


def test_time_series():

    fname = os.path.join('data', 'grids', 'IEEE39_1W.gridcal')
    print('Reading...')
    main_circuit = FileOpen(fname).open()

    pf_options = PowerFlowOptions(SolverType.NR,
                                  verbose=False,
                                  initialize_with_existing_solution=False,
                                  multi_core=False,
                                  dispatch_storage=True,
                                  control_q=ReactivePowerControlMode.NoControl,
                                  control_p=True)

    ts = TimeSeries(grid=main_circuit, options=pf_options, start_=0, end_=96)
    ts.run()

    data = open_data_frame_from_zip(file_name_zip=os.path.join('data', 'results', 'Results_IEEE39_1W.zip'),
                                    file_name='Time series Bus voltage module.csv')

    assert np.isclose(np.abs(ts.results.voltage), data.values[:96]).all()

    data = open_data_frame_from_zip(file_name_zip=os.path.join('data', 'results', 'Results_IEEE39_1W.zip'),
                                    file_name='Time series Branch active power "from".csv')

    assert np.isclose(np.real(ts.results.Sf), data.values[:96]).all()


if __name__ == '__main__':
    test_time_series()