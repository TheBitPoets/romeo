ARG PYTHON_BASE_IMAGE
FROM ${PYTHON_BASE_IMAGE}

LABEL org.opencontainers.image.title="Romeo untrusted submission runner" \
      io.thebitlab.runtime-id="romeo-sim" \
      io.thebitlab.worker-schemas="romeo.command_trace.v1,romeo.behavioural_result.v1"

COPY docker/runtime-runner/requirements.lock /tmp/requirements.lock
COPY pyproject.toml README.md /opt/romeo/
COPY src /opt/romeo/src
RUN python -m pip install --no-cache-dir --require-hashes -r /tmp/requirements.lock \
    && python -m pip install --no-cache-dir --no-deps --no-build-isolation /opt/romeo \
    && useradd --uid 65532 --create-home --shell /usr/sbin/nologin runner \
    && rm -f /tmp/requirements.lock
ENV PYTHONUTF8=1

WORKDIR /submission
USER runner
ENTRYPOINT ["python", "-I", "-m", "romeo.integrations.thebitlab.sandbox_worker"]
