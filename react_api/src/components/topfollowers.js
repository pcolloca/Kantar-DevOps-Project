import React from 'react'

const TopFollowers = ({followers_list}) => {
    return (
        <div class="list">
            {followers_list.map((twitter) => (
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">User: {twitter.user}</h5>
                        <h6 class="card-subtitle mb-2 text-muted">Followers: {twitter.followers}</h6>
                    </div>
                </div>
            ))}
        </div>
    )
};

export default TopFollowers