import React, { useState } from 'react'
import Popup from './Popup'

const PopupOperation = () => {
  const [showPopup, setShowPopup] = useState(false);

  return (
    <div>
      <div className="">
        <button
          className="bg-blue-500 text-white p-2 rounded"
          onClick={() => setShowPopup(true)}
        >
          Show Popup
        </button>
        {showPopup && <Popup onClose={() => setShowPopup(false)} />}
      </div>
    </div>
  )
}

export default PopupOperation