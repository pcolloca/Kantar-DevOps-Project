import React from 'react'

const PostLanguage = ({posts}) => {
    return (
        <div class="list">
            {posts.map((twitter) => (
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Hashtag: {twitter.hashtag}</h5>
                        <h6 class="card-subtitle">Language {twitter.language}</h6>
                        <h6 class="card-subtitle mb-2 text-muted">Posts: {twitter.posts}</h6>
                    </div>
                </div>
            ))}
        </div>
    )
};

export default PostLanguage