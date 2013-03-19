from culinary.mcbv.base import View, TemplateView, RedirectView
from culinary.mcbv.dates import (ArchiveIndexView, YearArchiveView, MonthArchiveView,
                                     WeekArchiveView, DayArchiveView, TodayArchiveView,
                                     DateDetailView)
from culinary.mcbv.detail import DetailView
from culinary.mcbv.edit import FormView, CreateView, UpdateView, DeleteView
from culinary.mcbv.list import ListView

__version__ = "0.3.1"

class GenericViewError(Exception):
    """A problem in a generic view."""
    pass
