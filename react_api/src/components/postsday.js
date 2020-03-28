import React from 'react'

const PostsDay = ({posts}) => {
    return (
        <div class="list">
            {posts.map((twitter) => (
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Date: {twitter.day + "/"+ twitter.month }</h5>
                        <h6 class="card-subtitle">Hour: {twitter.hour + ":00"}</h6>
                        <h6 class="card-subtitle">Posts: {twitter.posts}</h6>
                    </div>
                </div>
            ))}
        </div>
    )
};

export default PostsDay