import { useEffect, useState } from "react";
import axios from "axios";

const Reviews = ({ productId }) => {
  const [reviews, setReviews] = useState([]);
  const [newReview, setNewReview] = useState("");
  const [error, setError] = useState("");
  const [isEditing, setIsEditing] = useState(false);
  const [editReview, setEditReview] = useState("");
  const [reviewToEdit, setReviewToEdit] = useState(null);

  useEffect(() => {
    fetchReviews();
  }, [productId]);

  const fetchReviews = async () => {
    try {
      const response = await axios.get(`/reviews/product/${productId}`);
      setReviews(response.data);
    } catch (err) {
      setError("Failed to load reviews");
    }
  };

  const addReview = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.post(
        "/reviews/",
        { product_id: productId, text: newReview },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setReviews([...reviews, response.data]);
      setNewReview("");
    } catch (err) {
      setError("Failed to add review");
    }
  };

  const updateReview = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.put(
        `/reviews/${reviewToEdit.id}`,
        { text: editReview },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setReviews(
        reviews.map((review) =>
          review.id === reviewToEdit.id ? { ...review, text: editReview } : review
        )
      );
      setIsEditing(false);
      setEditReview("");
    } catch (err) {
      setError("Failed to update review");
    }
  };

  const deleteReview = async (reviewId) => {
    try {
      const token = localStorage.getItem("token");
      await axios.delete(`/reviews/${reviewId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setReviews(reviews.filter((review) => review.id !== reviewId));
    } catch (err) {
      setError("Failed to delete review");
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-4">Reviews</h2>
      {error && <p className="text-red-500">{error}</p>}

      {/* Список отзывов */}
      <ul>
        {reviews.map((review) => (
          <li key={review.id} className="flex justify-between p-2 border-b">
            <span>{review.text}</span>
            <div className="space-x-2">
              <button
                onClick={() => {
                  setIsEditing(true);
                  setReviewToEdit(review);
                  setEditReview(review.text);
                }}
                className="text-blue-500"
              >
                Edit
              </button>
              <button
                onClick={() => deleteReview(review.id)}
                className="text-red-500"
              >
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>

      {/* Добавление нового отзыва */}
      {!isEditing ? (
        <div className="mt-4">
          <textarea
            value={newReview}
            onChange={(e) => setNewReview(e.target.value)}
            className="border p-2 rounded w-full"
            placeholder="Write a review"
          />
          <button
            onClick={addReview}
            className="mt-2 bg-black text-white p-2 rounded"
          >
            Add Review
          </button>
        </div>
      ) : (
        <div className="mt-4">
          <textarea
            value={editReview}
            onChange={(e) => setEditReview(e.target.value)}
            className="border p-2 rounded w-full"
            placeholder="Edit your review"
          />
          <button
            onClick={updateReview}
            className="mt-2 bg-blue-500 text-white p-2 rounded"
          >
            Update Review
          </button>
        </div>
      )}
    </div>
  );
};

export default Reviews;
