import React from 'react';

/**
 *
 * @return {*} Intent Table component
 */
function IntentTable() {
  return (
    <div className="col-span-full xl:col-span-12 bg-white shadow-lg rounded-sm border border-slate-200">
      <header className="px-5 py-4 border-b border-slate-100">
        <h2 className="font-semibold text-slate-800">Intents</h2>
      </header>
      <div className="p-3">

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="table-auto w-full">
            {/* Table header */}
            <thead className="text-xs uppercase text-slate-400 bg-slate-50 rounded-sm">
              <tr>
                <th className="p-2">
                  <div className="font-semibold text-left">Intent Id</div>
                </th>
                <th className="p-2">
                  <div className="font-semibold text-center">Request Time</div>
                </th>
                <th className="p-2">
                  <div className="font-semibold text-center">Service</div>
                </th>
                <th className="p-2">
                  <div className="font-semibold text-center">Status</div>
                </th>
              </tr>
            </thead>
            {/* Table body */}
            <tbody className="text-sm font-medium divide-y divide-slate-100">
              {/* Row */}
              <tr>
                <td className="p-2">
                  <div className="flex items-center">
                    <div className="text-slate-800">Intent-300</div>
                  </div>
                </td>
                <td className="p-2">
                  <div className="text-center">12-12-2022 14:00</div>
                </td>
                <td className="p-2">
                  <div className="text-center text-green-500">360 Video </div>
                </td>
                <td className="p-2">
                  <div className="text-center text-sky-500">Delivered</div>
                </td>
              </tr>

            </tbody>
          </table>

        </div>
      </div>
    </div>
  );
}

export default IntentTable;
