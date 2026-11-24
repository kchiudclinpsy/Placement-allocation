# Data dictionary

## trainees.csv

- `trainee_id`: pseudonymous unique ID.
- `cohort_id`: cohort code.
- `training_year`: 1, 2 or 3.
- `next_placement_number`: 1 to 6.
- `base_code`: generic geographic base.
- `home_zone_code`: optional coarse zone, not a full address.
- `driving_access`: Yes, No or Adjustment.
- `max_commute_minutes`: approved operational threshold where applicable.
- `working_pattern_code`: full-time or approved pattern code.
- `allocation_status`: Active, Hold or ManualReview.

## placement_offers.csv

- `offer_id`, `placement_id`, `rotation_id`: unique time-bounded offer.
- `capacity`: available trainee places.
- `base_code`, `site_zone_code`: geographic coding.
- `placement_stage`: Core1, Core2, Specialist or Any.
- `approved`: Yes or No.
- `quality_status`: Green, Review or Suspended.
- `supervisor_approved`: Yes or No.
- `supervisor_training_valid_to`: date.
- `weekly_supervision_minutes`: planned protected supervision.
- `weekly_contact_minutes`: total supervisor contact.
- `cover_arrangement_confirmed`: Yes or No.
- `travel_required`, `pool_vehicle_available`: Yes or No.

## placement_capabilities.csv

One row per placement capability. `capability_type` can be ClientGroup, Setting, Presentation, Approach, Assessment, CoreCompetency or SpecialistExperience. `capability_code` uses a locally governed taxonomy. `opportunity_strength` is Introductory, Developing or Substantial.

## placement_history.csv

One row per completed or interrupted placement. Includes placement number, dates, outcome, attendance days, experience codes and whether competency evidence was signed off. Do not include patient-level data.

## competency_status.csv

One row per trainee and competency code. `status` is NotYetEvidenced, Developing, Achieved or RequiresRemediation. Include evidence date and source placement number, but not clinical narratives.

## specialist_preferences.csv

Used only for placement numbers 5 and 6. Includes trainee, rotation, placement, rank and advisor-review status. Choices must be distinct.

## review_flags.csv

Restricted file containing only coded flags, validity dates and review status. Examples: AdjustmentConstraint, OutOfBaseReview, CompetencyGap, PriorPlacementIncomplete, QualityHold and SafetyReview. Detailed evidence remains outside this toolkit.
