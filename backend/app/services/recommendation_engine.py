from app.models.metric import SearchTermMetric
from app.models.product import Product
from app.models.recommendation import Recommendation, RecommendationAction


MIN_CLICKS_FOR_NEGATIVE = 20
MIN_ORDERS_FOR_WINNER = 2
MIN_ORDERS_FOR_BID_INCREASE = 3


def build_recommendations(
    product: Product,
    metrics: list[SearchTermMetric],
) -> list[Recommendation]:
    recommendations: list[Recommendation] = []

    for metric in metrics:
        recommendation = analyze_metric(product, metric)

        if recommendation:
            recommendations.append(recommendation)

    return recommendations


def analyze_metric(product: Product, metric: SearchTermMetric) -> Recommendation | None:
    target_acos = product.target_acos_percent

    if metric.orders >= MIN_ORDERS_FOR_WINNER and metric.acos_percent is not None:
        if metric.acos_percent <= target_acos:
            return Recommendation(
                report_id=metric.report_id,
                metric_id=metric.id,
                action_type=RecommendationAction.MOVE_TO_EXACT.value,
                search_term=metric.search_term,
                campaign_name=metric.campaign_name,
                reason=(
                    f'Search term "{metric.search_term}" generated {metric.orders} orders '
                    f"with {metric.acos_percent}% ACOS, which is at or below your "
                    f"{target_acos}% target ACOS. Consider moving it to an exact match campaign."
                ),
                confidence=0.9,
            )

    if metric.clicks >= MIN_CLICKS_FOR_NEGATIVE and metric.sales == 0:
        return Recommendation(
            report_id=metric.report_id,
            metric_id=metric.id,
            action_type=RecommendationAction.ADD_NEGATIVE_EXACT.value,
            search_term=metric.search_term,
            campaign_name=metric.campaign_name,
            reason=(
                f'Search term "{metric.search_term}" received {metric.clicks} clicks '
                f"and spent {metric.spend}, but generated no sales. Consider adding it "
                f"as a negative exact keyword to reduce wasted spend."
            ),
            confidence=0.85,
        )

    if metric.sales > 0 and metric.acos_percent is not None:
        if metric.acos_percent > target_acos:
            return Recommendation(
                report_id=metric.report_id,
                metric_id=metric.id,
                action_type=RecommendationAction.REDUCE_BID.value,
                search_term=metric.search_term,
                campaign_name=metric.campaign_name,
                reason=(
                    f'Search term "{metric.search_term}" generated sales but ACOS is '
                    f"{metric.acos_percent}%, higher than your {target_acos}% target. "
                    f"Consider reducing bid or monitoring conversion quality."
                ),
                confidence=0.75,
            )

    if (
        metric.orders >= MIN_ORDERS_FOR_BID_INCREASE
        and metric.acos_percent is not None
        and metric.acos_percent < target_acos * 0.7
    ):
        return Recommendation(
            report_id=metric.report_id,
            metric_id=metric.id,
            action_type=RecommendationAction.INCREASE_BID.value,
            search_term=metric.search_term,
            campaign_name=metric.campaign_name,
            reason=(
                f'Search term "{metric.search_term}" has strong performance with '
                f"{metric.orders} orders and {metric.acos_percent}% ACOS. Consider "
                f"increasing bid carefully to capture more volume."
            ),
            confidence=0.8,
        )

    return None