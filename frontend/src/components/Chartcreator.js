import React from 'react'

const Chartcreator = () => {
  return (
    <div className='CreatorCharts border p-4 mb-4'>
      <h2 className="text-xl mb-4 text-center">Chart Creator</h2>

<select className="select select-bordered w-full max-w-xs mx-3">
  <option disabled selected>Select chart name</option>
  <option>Han Solo</option>
  <option>Greedo</option>
</select>
<select className="select select-bordered w-full max-w-xs mx-3">
  <option disabled selected>Select vue</option>
  <option>Han Solo</option>
  <option>Greedo</option>
</select>
<input type="text" placeholder="Id entreprise" className="input input-bordered w-full max-w-xs mr-5" />
<button type="button" className="px-4 py-2 bg-blue-500 text-white rounded">create chart</button>
    </div>
  )
}

export default Chartcreator
