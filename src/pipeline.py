import numpy as np
import lightkurve as lk

def fetch_and_clean_lightcurve(target_name, sector=None):
    """
    Downloads a light curve from MAST (supporting both TESS and Kepler)
    and flattens stellar noise.
    """
    try:
        # 1. First attempt: Search with specific sector / SPOC pipeline
        if sector and sector > 0:
            search = lk.search_lightcurve(target_name, sector=sector, author="SPOC")
            if len(search) == 0:
                search = lk.search_lightcurve(target_name, sector=sector)
        else:
            # 2. General search: Matches TESS, Kepler, and K2 targets
            search = lk.search_lightcurve(target_name, author="SPOC")
            if len(search) == 0:
                search = lk.search_lightcurve(target_name)
        
        if len(search) == 0:
            return None, None
        
        raw_lc = search[0].download()
        clean_lc = raw_lc.remove_nans().flatten(window_length=401)
        return raw_lc, clean_lc
    except Exception as e:
        print(f"Error downloading {target_name}: {e}")
        return None, None


def run_bls(lc, period_min=0.5, period_max=20.0, num_periods=3000):
    """
    Runs a Box Least Squares (BLS) periodogram to find the strongest transit signal.
    """
    period_grid = np.linspace(period_min, period_max, num_periods)
    bls = lc.to_periodogram(method='bls', period=period_grid)
    
    best_period = float(bls.period_at_max_power.value)
    best_t0 = float(bls.transit_time_at_max_power.value)
    
    return bls, best_period, best_t0


def extract_features(lc, period, t0):
    """
    Calculates the 5 numerical features required by the ML classifier.
    """
    time_span = lc.time.value[-1] - lc.time.value[0]
    transit_count = int(time_span / period)
    
    folded_lc = lc.fold(period=period, epoch_time=t0)
    flux = folded_lc.flux.value
    
    baseline_level = np.nanpercentile(flux, 50)
    dip_level = np.nanpercentile(flux, 1)
    signal_depth = baseline_level - dip_level
    
    noise = np.nanstd(flux[flux > np.nanpercentile(flux, 20)])
    snr = signal_depth / noise if noise > 0 else 0.0
    
    transit_epochs = np.round((lc.time.value - t0) / period)
    odd_mask = (transit_epochs % 2) != 0
    even_mask = (transit_epochs % 2) == 0
    
    odd_lc = lc[odd_mask].fold(period=period, epoch_time=t0)
    even_lc = lc[even_mask].fold(period=period, epoch_time=t0)
    
    odd_depth = 1.0 - np.nanpercentile(odd_lc.flux.value, 5) if len(odd_lc) > 0 else 0.0
    even_depth = 1.0 - np.nanpercentile(even_lc.flux.value, 5) if len(even_lc) > 0 else 0.0
    odd_even_diff = abs(odd_depth - even_depth)
    
    return {
        "period_days": round(float(period), 4),
        "transit_count": transit_count,
        "signal_depth": round(float(signal_depth), 5),
        "snr": round(float(snr), 2),
        "odd_even_diff": round(float(odd_even_diff), 6)
    }